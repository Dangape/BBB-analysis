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
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import spacy

nlp = spacy.load('en_core_web_sm')

nltk.download('vader_lexicon')
stopwords = nltk.corpus.stopwords.words('portuguese')
newStopWords = ['né','Se','De','q','vc','e','ter','ne','da','to','tô','o','O','https','t','BBB22','CO','tá',
                'dar','bbb22','TE','te','Eu','#BBB22','HTTPS','E','pra','tbm','tb','T','t','tt','ja','nao',
                '#bbb22','#redebbb','bbb','ai','desse','quis','d','voce','vai','ta','#bbb']
stopwords.extend(newStopWords)

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
n_tweets = int(100)

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
    # print(tweet.text)
    tweet_list.append(unidecode(tweet.text))
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

# #Removing RT, Punctuation etc
tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
remove_rt = lambda x: re.sub('RT @\w+: ',' ',x)
tags = lambda x: re.sub(' /<[^>]+>/',' ',x)
links = lambda x: re.sub(r"http\S+", ' ', x)
tw_list['text'] = tw_list.text.map(remove_rt).map(tags).map(links)
tw_list['text'] = tw_list.text.str.lower()
# Remove punctuation
# tw_list['text'] = tw_list['text'].str.replace('[^ws]', '', regex=True)
# Remove digits
text = tw_list['text'].str.replace('[d]+', '', regex=True)

print(tw_list.head(10))

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").\
    generate(str(tw_list['text'].values))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()