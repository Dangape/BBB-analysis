import tweepy
import pandas as pd
import tweepy
from config import create_api
from datetime import datetime,timezone,timedelta
import statistics
import pytz
import time
from sentiment import get_sentiment
from io import StringIO # python3; python2: BytesIO
import boto3
import numpy as np



consumer_key = 'AxrLnGCzWymdqtyaGyuPps5oa' #API key
consumer_secret = 'dDZP1s8kCO5fg2yM3sVv60cFb0Zhmj0DT2cgh5ZneJDUEerhQM' #API key secret
access_token = '1460657321839890436-ZnRI0HMOYTVNpWh7j0QIM4m62G4qCo' #Access token
access_token_secret = 'janLV9AZyllBqORJJfltkegaeYISDNTbflUZZtCLWmgEB' #Access token secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tz = pytz.timezone('America/Sao_Paulo')
today = datetime.now(tz=tz)
dt_string = today.strftime("%Y-%m-%d")

def count_rt_likes(user):
    likes = []
    rts = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
        if (datetime.now(timezone.utc) - tweet.created_at).days < 3:
            likes.append(tweet.favorite_count)
            rts.append(tweet.retweet_count)
        else:
            break

    return {'total_likes':sum(likes),'mean_likes': statistics.mean(likes),'mean_rts':statistics.mean(rts),'total_rts':sum(rts)}

players_twitter = ['PedroScooby','Aguiarthur','iampauloandre','linndaquebrada','LucasBissoli_',
                   'nataliadeodato','a_jessilane','gustavo_beats','eslomarques','vyniof','Silva_DG','dra_laiscaldass','eliezer']

players_instagram = ['pedroscooby','arthuraguiar','iampauloandre','linndaquebrada','bissolilucas','natalia.deodato',
                     'jessilane','gustavo_marsengo','eslomarques','vyniof','douglassilva','dra.laiscaldass','eliezer']

players_names = ['Pedro Scooby', 'Arthur Aguiar', 'Paulo André','Linna','Lucas','Natalia','Jessi','Gustavo','Eslovênia','Vyni','Douglas','Lais','Eliezer']

players_alias = ['scooby','arthur','pa','linna','lucas','nat','jessi','gustavo','eslo','vyni','dg','lais','eli']

instagram_followers = [4092508,12248481,5290181,2565581,881134,2746130,1053104,751474,2069427,4119570,2799711,1168689,968241] #tentar automatizar

data = pd.DataFrame(columns = ['alias','user_insta','followers_insta','user_tt','followers_tt','total_likes_5days',
                               'like_mean_5days','total_rts_5days','rt_mean_5days','sentiment','score','date'], index=players_names)

data['alias'] = players_alias
data['user_insta'] = players_instagram
data['user_tt'] = players_twitter
data['followers_insta'] = instagram_followers
data['date'] = dt_string


data['followers_tt'] = data.apply(lambda x: api.get_user(screen_name=str(x.user_tt)).followers_count, axis=1)
data['like_mean_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['mean_likes'], axis = 1)
data['rt_mean_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['mean_rts'], axis = 1)
data['total_likes_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['total_likes'], axis = 1)
data['total_rts_5days'] = data.apply(lambda x: count_rt_likes(x.user_tt)['total_rts'], axis = 1)


data['sentiment'] = data.apply(lambda x: get_sentiment(['{} #BBB22'.format(x.alias),'{} #bbb22'.format(x.alias)], 500), axis=1)

#new columns
data['rt_follower'] = data['total_rts_5days']/data['followers_tt']
data['likes_follower'] = data['total_likes_5days']/data['followers_tt']

data['score'] = ((1.5*data['rt_mean_5days'] + data['like_mean_5days'])/data['followers_tt'])^data['sentiment']

# create excel writer object
dt_string = today.strftime("%Y_%m_%d")
file_name = 'social_data_'+dt_string+'.xlsx'
data.to_csv(file_name, sep=',')


bucket = 'tweet-bot-data' # already created on S3
csv_buffer = StringIO()
data.to_csv(csv_buffer)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, 'social_data/'+file_name+'.csv').put(Body=csv_buffer.getvalue())