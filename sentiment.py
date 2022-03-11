import tweepy
import pandas as pd
import nltk
import re
from unidecode import unidecode
from wordcloud import WordCloud
from nltk.corpus import stopwords
import logging
import matplotlib.pyplot as plt
import spacy
import logging
from config import create_api, remove_hashtag_and_mention
from datetime import datetime

nlp = spacy.load('en_core_web_sm')
nltk.download('vader_lexicon')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

api = create_api()
keyword = '#BBB22 OR #bbb22'
n_tweets = 1000

stopwords = nltk.corpus.stopwords.words('portuguese')
newStopWords = ['né','Se','q','vc','ter','ne','da','to','tô','https','BBB22','tá',
                'dar','bbb22','te','eu','#BBB22','HTTPS','pra','tbm','tb','tt','ja','nao',
                '#bbb22','#redebbb','bbb','ai','desse','quis','voce','vai','ta','#bbb','ela','sobre','cada','ah','mas','mais',
                'pro','dela','vem','ja','outra','porque','por que','por quê','porquê','bem','rt','todo','tao','acho','sao','voces','pq',
                'co','t','n','desde','so','mim','la','quer','fez','agora','aqui','vcs','gente','deu', 'ate', 'oq', 'ser', 'kkk','kk','kkkk','kkkkk','kkkkkk']

stopwords.extend(newStopWords)
tweet_list = []

def create_wc():
    logger.info("Getting tweets")
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang = 'pt').items(n_tweets):
        tweet_list.append(unidecode(tweet.text))
    # #cleaning tweets
    tw_list = pd.DataFrame(tweet_list)
    tw_list.drop_duplicates(inplace=True)
    tw_list['original'] = tw_list[0]
    tw_list['text'] = tw_list[0]

    # Lowercase
    tw_list['text'] = tw_list.text.str.lower()

    #Remove RT
    remove_rt = lambda x: re.sub('rt @\w+: ', ' ', x)

    #Remove tags
    tags = lambda x: re.sub(' /<[^>]+>/', ' ', x)

    #Remove links
    links = lambda x: re.sub(r'http\S+',' ',x)


    tw_list['text'] = tw_list.text.map(remove_rt)
    tw_list['text'] = tw_list.text.map(tags)
    tw_list['text'] = tw_list.text.map(links)

    # Remove stopwords
    tw_list['text'] = tw_list['text'].apply(lambda x: remove_hashtag_and_mention(x))

    #Remove stopwords
    tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([x.strip() for x in x.split() if x not in stopwords]))

    # create excel writer object
    writer = pd.ExcelWriter('output.xlsx')
    tw_list.to_excel(writer, engine='xlsxwriter')
    writer.save()

