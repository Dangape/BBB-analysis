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
