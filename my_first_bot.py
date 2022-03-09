import tweepy
import pandas as pd
import nltk
import re
from unidecode import unidecode
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import spacy
import logging
from config import create_api
import schedule
from datetime import datetime, date

nlp = spacy.load('en_core_web_sm')
nltk.download('vader_lexicon')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

stopwords = nltk.corpus.stopwords.words('portuguese')
newStopWords = ['né','Se','De','q','vc','e','ter','ne','da','to','tô','o','O','https','t','BBB22','CO','tá',
                'dar','bbb22','TE','te','Eu','#BBB22','HTTPS','E','pra','tbm','tb','T','t','tt','ja','nao',
                '#bbb22','#redebbb','bbb','ai','desse','quis','d','voce','vai','ta','#bbb','ela','sobre','cada','ah','mas','mais',
                'pro','dela','vem','ja','o','outra','porque','por que','por quê','porquê','bem','rt','todo','tao']

stopwords.extend(newStopWords)
tweet_list = []


# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

def create_wc(api,keyword,n_tweets):
    logger.info("Getting tweets")
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang = 'pt').items(n_tweets):
        tweet_list.append(unidecode(tweet.text))
    # #cleaning tweets
    tw_list = pd.DataFrame(tweet_list)
    tw_list.drop_duplicates(inplace=True)
    tw_list['text'] = tw_list[0]

    # Lowercase
    tw_list['text'] = tw_list.text.str.lower()

    #Remove stopwords
    tw_list['text'] = tw_list['text'].apply(
        lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))

    #Remove RT
    remove_rt = lambda x: re.sub('RT @\w+: ', ' ', x)

    #Remove tags
    tags = lambda x: re.sub(' /<[^>]+>/', ' ', x)

    #Remove links
    links = lambda x: re.sub(r"http\S+", ' ', x)

    tw_list['text'] = tw_list.text.map(remove_rt).map(tags).map(links)
    # # Remove digits
    # text = tw_list['text'].str.replace('[d]+', '', regex=True)

    # create a wordcloud
    logger.info("Generating WC")
    wc = WordCloud(background_color='white',
                   collocations=False,
                   width=400,
                   height=300,
                   contour_width=3,
                   contour_color='black',
                   stopwords=stopwords).generate(str(tw_list['text'].values))
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('wordcloud.png')

    logger.info("Tweetting")
    media_list = list()
    response = api.media_upload('wordcloud.png')
    media_list.append(response.media_id_string)

    status = 'BBB em: ' + dt_string
    api.update_status(status = status,media_ids=media_list)




# def main():
api = create_api()
create_wc(api,'#BBB22',500)
logger.info('Tweeted with success!!')
    # while True:
    #     create_wc(api)
    #     logger.info("Waiting...")
    #     time.sleep(60)

# schedule.every(1).minutes.do(create_wc(api,'#BBB22',200))
# while True:
#     schedule.run_pending()
#     time.sleep(1)



