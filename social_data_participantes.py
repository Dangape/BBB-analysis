import tweepy
import pandas as pd
import tweepy
from config import create_api
from datetime import datetime,timezone,timedelta
import statistics
import pytz
from io import StringIO
import boto3
import json
import instagramy

tz = pytz.timezone('America/Sao_Paulo')
today = datetime.now(tz=tz)
dt_string = today.strftime("%d/%m")

players_twitter = ['PedroScooby','Aguiarthur','iampauloandre','linndaquebrada','LucasBissoli_',
                   'nataliadeodato','a_jessilane','gustavo_beats','eslomarques','Silva_DG','dra_laiscaldass','eliezer']

players_instagram = ['pedroscooby','arthuraguiar','iampauloandre','linndaquebrada','bissolilucas','natalia.deodato',
                     'jessilane','gustavo_marsengo','eslomarques','douglassilva','dra.laiscaldass','eliezer']

players_names = ['Pedro Scooby', 'Arthur Aguiar', 'Paulo André','Linna','Lucas','Natalia','Jessi','Gustavo','Eslovênia','Douglas','Lais','Eliezer']

players_alias = ['scooby','arthur','pa','lina','lucas','nat','jessi','gustavo','eslo','dg','lais','eli']

def handler(event, context):
    generate_engagement()
    return {
        'statusCode': 200,
        'body': json.dumps('Tweet with Success using AWS Lambda!')
    }

def generate_engagement():
    api = create_api()

    def count_rt_likes(user):
        likes = []
        rts = []
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
            if (datetime.now(timezone.utc) - tweet.created_at).days < 2:
                likes.append(tweet.favorite_count)
                rts.append(tweet.retweet_count)

            else:
                break
        return {'total_likes':sum(likes),'mean_likes': statistics.mean(likes),'mean_rts':statistics.mean(rts),'total_rts':sum(rts)}

    def insta_data(user):
        session_id = "52422948190:3Z9eMGzKFWzeNY:1"
        data = instagramy.InstagramUser(user, sessionid=session_id)
        n_followers = data.number_of_followers
        posts = data.posts
        likes = []
        comments = []
        for post in posts:
            likes.append(post.likes)
            comments.append(post.comments)
        return {'n_followers': n_followers, 'mean_likes': statistics.mean(likes[-5:]), 'mean_comments': statistics.mean(comments[-5:])}

    data = pd.DataFrame(columns = ['alias','user_insta','user_tt','followers_insta','followers_tt','total_likes_tt',
                                   'like_mean_tt','total_rts_tt','rt_mean_tt','likes_mean_insta','comments_mean_insta','score','date'], index=players_names)

    data['alias'] = players_alias
    data['user_insta'] = players_instagram
    data['user_tt'] = players_twitter
    data['date'] = dt_string

    data['followers_tt'] = data.apply(lambda x: api.get_user(screen_name=str(x.user_tt)).followers_count, axis=1)
    data['followers_insta'] = data.apply(lambda x: insta_data(x.user_insta)['n_followers'], axis=1)
    data['likes_mean_insta'] = data.apply(lambda x: insta_data(x.user_insta)['mean_likes'], axis=1)
    data['comments_mean_insta'] = data.apply(lambda x: insta_data(x.user_insta)['mean_comments'], axis=1)
    data['like_mean_tt'] = data.apply(lambda x: count_rt_likes(x.user_tt)['mean_likes'], axis = 1)
    data['rt_mean_tt'] = data.apply(lambda x: count_rt_likes(x.user_tt)['mean_rts'], axis = 1)
    data['total_likes_tt'] = data.apply(lambda x: count_rt_likes(x.user_tt)['total_likes'], axis = 1)
    data['total_rts_tt'] = data.apply(lambda x: count_rt_likes(x.user_tt)['total_rts'], axis = 1)

    #calculating score
    # data['score'] = (data['like_mean_tt'] +1.5*data['rt_mean_tt'])*(1+(1/data['followers_tt']))
    data['score'] = ((data['like_mean_tt']+data['rt_mean_tt'])/data['followers_tt'])+\
                    ((data['likes_mean_insta']+data['comments_mean_insta'])/data['followers_insta'])
    data['score'] = data['score']*1000

    # check files already in bucket
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('tweet-bot-data')
    objects = []
    for my_bucket_object in my_bucket.objects.all():
        objects.append(my_bucket_object.key)

    # save to s3
    file_name = 'new_social_data.csv'
    bucket = 'tweet-bot-data'

    if 'social_data/' + file_name in objects:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key='social_data/' + file_name)
        actual_df = pd.read_csv(obj['Body'])
        actual_df = pd.concat([actual_df, data])
        csv_buffer = StringIO()
        actual_df.to_csv(csv_buffer, index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, 'social_data/' + file_name).put(Body=csv_buffer.getvalue())

    else:
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, 'social_data/' + file_name).put(Body=csv_buffer.getvalue())

# generate_engagement()