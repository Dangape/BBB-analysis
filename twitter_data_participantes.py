import tweepy
import pandas as pd
import tweepy
from config import create_api
from datetime import datetime,timezone,timedelta
import statistics
import pytz
from io import StringIO # python3; python2: BytesIO
import boto3
import json
tz = pytz.timezone('America/Sao_Paulo')
today = datetime.now(tz=tz)
dt_string = today.strftime("%Y-%m-%d")

players_twitter = ['PedroScooby','Aguiarthur','iampauloandre','linndaquebrada','LucasBissoli_',
                   'nataliadeodato','a_jessilane','gustavo_beats','eslomarques','vyniof','Silva_DG','dra_laiscaldass','eliezer']

players_instagram = ['pedroscooby','arthuraguiar','iampauloandre','linndaquebrada','bissolilucas','natalia.deodato',
                     'jessilane','gustavo_marsengo','eslomarques','vyniof','douglassilva','dra.laiscaldass','eliezer']

players_names = ['Pedro Scooby', 'Arthur Aguiar', 'Paulo André','Linna','Lucas','Natalia','Jessi','Gustavo','Eslovênia','Vyni','Douglas','Lais','Eliezer']

players_alias = ['scooby','arthur','pa','lina','lucas','nat','jessi','gustavo','eslo','vyni','dg','lais','eli']

def handler(event, context):
    gather_data('#ForaScooby OR #ForaVyni OR #ForaViny OR #ForaGustavo OR #BBB22 OR #bbb22',1000)
    return {
        'statusCode': 200,
        'body': json.dumps('Tweet with Success using AWS Lambda!')
    }


def count_rt_likes(user):
    likes = []
    rts = []
    api = create_api()
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
        if (datetime.now(timezone.utc) - tweet.created_at).days < 3:
            likes.append(tweet.favorite_count)
            rts.append(tweet.retweet_count)
        else:
            break

    return {'total_likes':sum(likes),'mean_likes': statistics.mean(likes),'mean_rts':statistics.mean(rts),'total_rts':sum(rts)}

data = pd.DataFrame(columns = ['alias','user_insta','user_tt','followers_tt','total_likes_5days',
                               'like_mean_5days','total_rts_5days','rt_mean_5days','score','date'], index=players_names)

data['alias'] = players_alias
data['user_insta'] = players_instagram
data['user_tt'] = players_twitter
data['date'] = dt_string


data['followers_tt'] = data.apply(lambda x: api.get_user(screen_name=str(x.user_tt)).followers_count, axis=1)
data['like_mean_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['mean_likes'], axis = 1)
data['rt_mean_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['mean_rts'], axis = 1)
data['total_likes_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['total_likes'], axis = 1)
data['total_rts_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['total_rts'], axis = 1)


# data['sentiment'] = data.apply(lambda x: get_sentiment(['{} #BBB22'.format(x.alias),'{} #bbb22'.format(x.alias)], 500), axis=1)

#new columns
data['rt_follower'] = data['total_rts_5days']/data['followers_tt']
data['likes_follower'] = data['total_likes_5days']/data['followers_tt']

#calculating score
data['score'] = (data['like_mean_5days'] + 1.5*data['rt_mean_5days'])*(1+((data['total_likes_5days']+1.5*data['total_rts_5days'])/data['followers_tt']))

# check files already in bucket
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('tweet-bot-data')
objects = []
for my_bucket_object in my_bucket.objects.all():
    objects.append(my_bucket_object.key)

# save to s3
file_name = 'social_data.csv'
bucket = 'tweet-bot-data'

if 'social_data/' + file_name in objects:
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key='social_data/' + file_name)
    actual_df = pd.read_csv(obj['Body'])
    actual_df = pd.concat([actual_df, data])
    csv_buffer = StringIO()
    actual_df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, 'social_data/' + file_name).put(Body=csv_buffer.getvalue())

else:
    csv_buffer = StringIO()
    data.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, 'social_data/' + file_name).put(Body=csv_buffer.getvalue())