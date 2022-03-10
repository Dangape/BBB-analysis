import tweepy
import pandas as pd
import nltk
import re
from unidecode import unidecode
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import spacy
import logging
from config import create_api
from datetime import datetime
import schedule
import time

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
                'co','t','n','desde','so','mim''la','quer','fez','agora','aqui','vcs','gente','deu', 'ate', 'sim']

stopwords.extend(newStopWords)
tweet_list = []

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

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
    links = lambda x: re.sub('/(?:https?|ftp):\/\/[\n\S]+/g', ' ', x)
    hashtags = lambda x: re.sub('/\#\w\w+\s?/g', ' ', x)
    mentions = lambda x: re.sub('/\@\w\w+\s?/g', ' ', x)
    laughts_ha = lambda x: re.sub('\b(?:a*(?:ha)+h?|(?:l+o+)+l+)\b', ' ', x)
    laughts_k = lambda x: re.sub('\b(?:k*(?:k)+k?|(?:l+o+)+l+)\b', ' ', x)

    tw_list['text'] = tw_list.text.map(remove_rt)
    tw_list['text'] = tw_list.text.map(tags)
    tw_list['text'] = tw_list.text.map(links)
    tw_list['text'] = tw_list.text.map(hashtags)
    tw_list['text'] = tw_list.text.map(mentions)
    tw_list['text'] = tw_list.text.map(laughts_ha)
    tw_list['text'] = tw_list.text.map(laughts_k)

    #Remove stopwords
    tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([x.strip() for x in x.split() if x not in stopwords]))

    # create excel writer object
    writer = pd.ExcelWriter('output.xlsx')
    tw_list.to_excel(writer, engine='xlsxwriter')
    writer.save()

    # create a wordcloud
    logger.info("Generating WC")
    wc = WordCloud(background_color='white',
                   collocations=False,
                   width=1600,
                   height=800,
                   contour_width=3,
                   contour_color='black',
                   stopwords=stopwords).generate(str(tw_list['text'].values))
    plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight')

    logger.info("Tweetting")
    media_list = list()
    response = api.media_upload('wordcloud.png')
    media_list.append(response.media_id_string)

    status = 'BBB em: ' + dt_string
    api.update_status(status = status,media_ids=media_list)

# The Scheduling is happening below:
schedule.every().day.at("10:30").do(create_wc)
schedule.every().day.at("21:30").do(create_wc)
schedule.every().day.at("23:00").do(create_wc)
schedule.every().day.at("23:30").do(create_wc)
schedule.every().day.at("00:30").do(create_wc)


while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except:
        print('Error...')
        time.sleep(120)


