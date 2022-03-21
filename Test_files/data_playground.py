import boto3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil import tz as timezone
import pytz
import time
import base64
import requests
import hmac
import json
from bs4 import BeautifulSoup
import re
import instagramy

# def read_s3_csv(bucket, file_path):
#     s3 = boto3.client('s3')
#     obj = s3.get_object(Bucket=bucket, Key=file_path)
#     df = pd.read_csv(obj['Body'])
#     return df
#
# def convert_utc(row):
#     from_zone = timezone.gettz('UTC')
#     to_zone = timezone.gettz('America/Sao_Paulo')
#     utc = datetime.strptime( row['created_at'], "%d/%m/%Y %H:%M:%S")
#     utc = utc.replace(tzinfo=from_zone)
#     central = utc.astimezone(to_zone)
#     return central.strftime("%d/%m/%Y %H:%M:%S")
#
# bucket = 'tweet-bot-data'
# file_path = 'social_data/paredao.csv'
#
# df = read_s3_csv(bucket, file_path)
# df['created_at'] = df.apply(lambda x: convert_utc(x), axis=1)
# df['paredao'].fillna('', inplace=True)
#
# # treat similar names
# df['paredao'] = df['paredao'].apply(lambda x: ' '.join([word.replace('viny', 'vyni') for word in x.split()]))
# df['paredao'] = df['paredao'].apply(lambda x: ' '.join([word.replace('eslovenia', 'eslo') for word in x.split()]))
# df['paredao'] = df['paredao'].apply(lambda x: ' '.join([word.replace('linn', 'linna') for word in x.split()]))
# df = df[df['paredao'] != '']
# df = pd.DataFrame(df[df['paredao'] != '']['paredao'].value_counts(normalize=True).sort_values(ascending=False))
# print(df)
# df.reset_index(inplace=True)

# writer = pd.ExcelWriter('tweets_data.xlsx')
# df.to_excel(writer)
# writer.save()

social_data = pd.read_csv('social_data.csv')
# fh= pd.read_csv('followers_history.csv',sep=';')

social_data['date'] = pd.to_datetime(social_data['date']).dt.strftime('%d/%m')
players_instagram = ['pedroscooby','arthuraguiar','iampauloandre','linndaquebrada','bissolilucas','natalia.deodato',
                     'jessilane','gustavo_marsengo','eslomarques','douglassilva','dra.laiscaldass','eliezer']

# Connecting the profile
session_id = "52422948190:3Z9eMGzKFWzeNY:1"
df = pd.DataFrame(columns=['user_insta','likes_insta', 'comments_insta', 'date', 'followers'])

for player in players_instagram:
    user = instagramy.InstagramUser(player,sessionid=session_id)
    n_followers = user.number_of_followers
    posts = user.posts
    listdict = []
    for post in posts:
        listdict.append({'user_insta': player, 'likes_insta':post.likes, 'comments_insta':post.comments,
                         'date':post.taken_at_timestamp.strftime("%d/%m")})
    df = df.append(listdict, ignore_index=True)

social_data = pd.merge(social_data,df.groupby(by=['user_insta','date'],as_index=False).agg({'likes_insta':'sum','comments_insta':'sum'}),on=['user_insta','date'],how='left')

writer = pd.ExcelWriter('social_insta.xlsx')
social_data.to_excel(writer)
writer.save()