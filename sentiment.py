import tweepy
import pandas as pd
import nltk
import re
from unidecode import unidecode
from nltk.corpus import stopwords
import spacy
import logging
from config import create_api, remove_hashtag_and_mention
from deep_translator import GoogleTranslator
from textblob import TextBlob as tb
import numpy as np
import time
import string

nlp = spacy.load('en_core_web_sm')
nltk.download('vader_lexicon')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

api = create_api()


stopwords = nltk.corpus.stopwords.words('portuguese')
newStopWords = ['né', 'Se', 'q', 'vc', 'ter', 'ne', 'da', 'to', 'tô', 'https', 'BBB22', 'tá',
                'dar', 'bbb22', 'te', 'eu', '#BBB22', 'HTTPS', 'pra', 'tbm', 'tb', 'tt', 'ja', 'nao',
                '#bbb22', '#redebbb', 'bbb', 'ai', 'desse', 'quis', 'voce', 'vai', 'ta', '#bbb', 'ela', 'sobre', 'cada',
                'ah', 'mas', 'mais',
                'pro', 'dela', 'vem', 'ja', 'outra', 'porque', 'por que', 'por quê', 'porquê', 'bem', 'rt', 'todo',
                'tao', 'acho', 'sao', 'voces', 'pq',
                'co', 't', 'n', 'desde', 'so', 'mim', 'la', 'quer', 'fez', 'agora', 'aqui', 'vcs', 'gente', 'deu',
                'ate', 'oq', 'ser', 'kkk', 'kk', 'kkkk', 'kkkkk', 'kkkkkk']

stopwords.extend(newStopWords)
tweet_list = {'text':[],'created_at':[]}

def get_sentiment(keyword,n_tweets):
    score = []
    logger.info("Getting tweets")
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang='pt',tweet_mode="extended").items(n_tweets):
        tweet_list['text'].append(unidecode(tweet.full_text))
        tweet_list['created_at'].append(pd.to_datetime(tweet.created_at).strftime("%d/%m/%Y %H:%M:%S"))

    # #cleaning tweets
    # tw_list = pd.DataFrame(tweet_list)
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

    tw_list['en_text'] = tw_list['text'].apply(lambda x: GoogleTranslator(source='auto', target='en').translate(x))
    # remove punctuation
    table = str.maketrans('', '', string.punctuation)
    tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([x.translate(table) for x in x.split()]))

    logger.info("Getting polarity...")
    for tweet in tw_list['en_text']:
        analysis = tb(tweet)
        polarity = analysis.sentiment.polarity
        score.append(polarity)

    logger.info("Success!!")
    time.sleep(300)
    return np.mean(score)

# tw_list = get_sentiment(['arthur #BBB22','arthur #bbb22'],5)



