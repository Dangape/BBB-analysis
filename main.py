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
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

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

# #cleaning tweets
tweet_list.drop_duplicates(inplace=True)
#Creating new dataframe and new features
tw_list = pd.DataFrame(tweet_list)
tw_list['text'] = tw_list[0]
#
# #Removing RT, Punctuation etc
# remove_rt = lambda x: re.sub('RT @\w+: ',' ',x)
# rt = lambda x: re.sub('(@[A-Za-z0–9]+)|([⁰-9A-Za-z \t])|(\w+:\/\/\S+)',' ',x)
# tw_list['text'] = tw_list.text.map(remove_rt).map(rt)
# tw_list['text'] = tw_list.text.str.lower()
# print(tw_list.head(10))

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(str(tw_list['text'].values))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()