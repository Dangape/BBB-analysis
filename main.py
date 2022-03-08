from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from unidecode import unidecode
from google_trans_new import google_translator
from PIL import Image

nltk.download('vader_lexicon')
translator = google_translator()

# Authentication
consumerKey = 'evXPxqc9rF72M6OCtdeRgDUTQ' #API key
consumerSecret = 'QUXXY5hs7fBxf53rPcWyUUZtHE7R2AyWiovfpM6WRrrz3zn7Bk' #API key secret
accessToken = '1460657321839890436-vgkxoPFmv96DsEZfbETzQykdEgMOWM' #Access token
accessTokenSecret = 'U8gIMhZ5UsHLz4fRJfItJlQhyw2PMxUyGWVnmb4w5wCH1' #Access token secret

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# Sentiment Analysisdef percentage(part,whole):
def percentage(part,whole):
 return 100 * float(part)/float(whole)

keyword = ['#BBB22']
n_tweets = int(20)

tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang = 'pt').items(n_tweets)

positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

#Contadores
numPos = 0
numNeg = 0
total = 0

# #Buscando tweets
for tweet in tweets:
    print(tweet.text)
    tweet_list.append(tweet.text)
    analysis = TextBlob(tweet.text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity
    if neg > pos:
        negative_list.append(tweet.text)
        negative += 1
    elif pos > neg:
        positive_list.append(tweet.text)
        positive += 1

    elif pos == neg:
        neutral_list.append(tweet.text)
        neutral += 1
        positive = percentage(positive, n_tweets)

negative = percentage(negative, n_tweets)
neutral = percentage(neutral, n_tweets)
polarity = percentage(polarity, n_tweets)

positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

tweet_list = pd.DataFrame(tweet_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)

def create_wordcloud(text):
    mask = np.array(Image.open('cloud.png'))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color='white',
    mask = mask,
    max_words=3000,
    stopwords=stopwords,
    repeat=True)
    wc.generate(str(text))
    wc.to_file('wc.png')
    print('Word Cloud Saved Successfully')
    path='wc.png'
    display(Image.open(path))

 # Creating wordcloud for positive sentiment
 create_wordcloud(tweet_list['text'].values)