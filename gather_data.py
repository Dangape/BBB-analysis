import tweepy
import pandas as pd
import re
from unidecode import unidecode
from config import create_api, remove_hashtag_and_mention
import numpy as np
import nltk
import string
from datetime import datetime
import pytz
from io import StringIO
import boto3
import json

nltk.data.path.append("/tmp")
nltk.download('stopwords',download_dir = "/tmp")

stopwords = nltk.corpus.stopwords.words('portuguese')
newStopWords = ['né', 'Se', 'q', 'vc', 'ter', 'ne', 'da', 'to', 'tô', 'https', 'BBB22', 'tá',
                'dar', 'bbb22', 'te', 'eu', '#BBB22', 'HTTPS', 'pra', 'tbm', 'tb', 'tt', 'ja', 'nao',
                '#bbb22', '#redebbb', 'bbb', 'ai', 'desse', 'quis', 'voce', 'vai', 'ta', '#bbb', 'ela', 'sobre',
                'cada', 'ah', 'mas', 'mais','pro', 'dela', 'vem', 'ja', 'outra', 'porque',
                'por que', 'por quê', 'porquê', 'bem', 'rt', 'todo','tao', 'acho', 'sao', 'voces', 'pq',
                'co', 't', 'n', 'desde', 'so', 'mim', 'la', 'quer', 'fez', 'agora', 'aqui', 'vcs', 'gente', 'deu',
                'ate', 'oq', 'ser', 'kkk', 'kk','kkkk', 'kkkkk', 'kkkkkk', 'kkkkkkkkk', 'kkkkk', 'kkkkkkk', 'kkkkkkkk',
                'fazendo', 'estao', 'hoje','fazer', 'nessa', 'ainda', 'diz', 'pois', 'falando', 'disse', 'dessa', 'p', 'x']

stopwords.extend(newStopWords)

def handler(event, context):
    gather_data('#ForaScooby OR #ForaVyni OR #ForaViny OR #ForaGustavo OR #BBB22 OR #bbb22 OR #forajessi OR '
                '#foraeli OR #foraeliezer OR #foraeslo OR #foraeslovenia OR #foravyni OR #foraviny OR #forapa OR '
                '#forapauloandre OR #foradg OR #foradouglas OR #foradouglassilva OR #foraarthur OR #forarrthur OR #foralina OR '
                '#foralinn OR #foralinna OR #foralucas OR #forabarao OR #foranatalia OR #foragustavo OR #foralais OR #forascooby',800)
    return {
        'statusCode': 200,
        'body': json.dumps('Tweet with Success using AWS Lambda!')
    }

def gather_data(keyword,n_tweets):
    api = create_api()
    tweet_list = {'text':[],'created_at':[],'updated_at':[]}
    paredao = ['#forajessi', '#foraeli', '#foraeliezer', '#foraeslo', '#foraeslovenia', '#foravyni', '#foraviny',
               '#forapa', '#forapauloandre', '#foradg', '#foradouglas', '#foradouglassilva', '#foraarthur',
               '#forarrthur', '#foralina', '#foralinn', '#foralinna', '#foralucas', '#forabarao', '#foranatalia',
               '#foragustavo', '#foralais', '#forascooby']

    # datetime object containing current date and time
    tz = pytz.timezone('America/Sao_Paulo')
    ct = datetime.now(tz=tz)
    dt_string = ct.strftime("%d/%m/%Y %H:%M:%S")

    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang='pt',tweet_mode="extended").items(n_tweets):
        tweet_list['text'].append(unidecode(tweet.full_text))
        tweet_list['created_at'].append(pd.to_datetime(tweet.created_at).strftime("%d/%m/%Y %H:%M:%S"))
        tweet_list['updated_at'].append(dt_string)

    #cleaning tweets
    tw_list = pd.concat({k: pd.Series(v) for k, v in tweet_list.items()}, axis=1)
    tw_list.drop_duplicates(inplace=True)

    # Lowercase
    tw_list['original'] = tw_list['text']
    tw_list['text'] = tw_list.text.str.lower()

    # Remove RT
    remove_rt = lambda x: re.sub('rt @\w+: ', ' ', x)

    # Remove tags
    tags = lambda x: re.sub(' /<[^>]+>/', ' ', x)

    # Remove links
    links = lambda x: re.sub(r'http\S+', ' ', x)

    tw_list['text'] = tw_list.text.map(remove_rt)
    tw_list['text'] = tw_list.text.map(tags)
    tw_list['text'] = tw_list.text.map(links)

    # Remove stopwords
    tw_list['text'] = tw_list['text'].apply(lambda x: remove_hashtag_and_mention(x))

    # Remove stopwords
    tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([x.strip() for x in x.split() if x not in stopwords]))

    # remove punctuation
    table = str.maketrans('', '', string.punctuation)
    tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([x.translate(table) for x in x.split()]))

    def check_paredao(row):
        for word in paredao:
            if word in row['original'].lower():
                return ' ' + word
            else:
                continue

    tw_list['paredao'] = tw_list.apply(lambda x: check_paredao(x), axis=1)
    tw_list['paredao'].fillna(' ', inplace=True)

    # treat similar names
    tw_list['paredao'] = tw_list['paredao'].apply(lambda x: ' '.join([word.replace('viny', 'vyni') for word in x.split()]))

    #check files already in bucket
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('tweet-bot-data')
    objects = []
    for my_bucket_object in my_bucket.objects.all():
        objects.append(my_bucket_object.key)

    #save to s3
    file_name = 'paredao.csv'
    bucket = 'tweet-bot-data'

    if 'social_data/' + file_name in objects:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key='social_data/' + file_name)
        actual_df = pd.read_csv(obj['Body'])
        actual_df = pd.concat([actual_df,tw_list])
        actual_df.drop_duplicates(subset='original', keep="last", inplace=True)
        csv_buffer = StringIO()
        actual_df.to_csv(csv_buffer, index = False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, 'social_data/' + file_name).put(Body=csv_buffer.getvalue())

    else:
        csv_buffer = StringIO()
        tw_list.to_csv(csv_buffer, index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, 'social_data/' + file_name).put(Body=csv_buffer.getvalue())

