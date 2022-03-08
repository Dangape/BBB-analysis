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

keyword = '#BBB22'
n_tweets = int(5)

tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(n_tweets)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

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

print('total number: ',len(tweet_list))
print('positive number: ',len(positive_list))
print('negative number: ', len(negative_list))
print('neutral number: ',len(neutral_list))