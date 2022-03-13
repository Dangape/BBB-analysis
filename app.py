
import json
import tweepy
import re
from unidecode import unidecode
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from datetime import datetime
import nltk
import pandas as pd
import io
import pytz
import string

consumer_key = 'AxrLnGCzWymdqtyaGyuPps5oa'  # API key
consumer_secret = 'dDZP1s8kCO5fg2yM3sVv60cFb0Zhmj0DT2cgh5ZneJDUEerhQM' # API key secret
access_token = '1460657321839890436-ZnRI0HMOYTVNpWh7j0QIM4m62G4qCo'  # Access token
access_token_secret ='janLV9AZyllBqORJJfltkegaeYISDNTbflUZZtCLWmgEB'  # Access token secret

# logger = logging.getLogger()
nltk.data.path.append("/tmp")
nltk.download('stopwords',download_dir = "/tmp")

stopwords = nltk.corpus.stopwords.words('portuguese')
newStopWords = ['né','Se','q','vc','ter','ne','da','to','tô','https','BBB22','tá',
                'dar','bbb22','te','eu','#BBB22','HTTPS','pra','tbm','tb','tt','ja','nao',
                '#bbb22','#redebbb','bbb','ai','desse','quis','voce','vai','ta','#bbb','ela','sobre','cada','ah','mas','mais',
                'pro','dela','vem','ja','outra','porque','por que','por quê','porquê','bem','rt','todo','tao','acho','sao','voces','pq',
                'co','t','n','desde','so','mim','la','quer','fez','agora','aqui','vcs','gente','deu', 'ate', 'oq', 'ser', 'kkk','kk',
                'kkkk','kkkkk','kkkkkk','fazendo','estao','hoje','fazer','nessa','ainda','diz','pois']

stopwords.extend(newStopWords)

def handler(event, context):
    # TODO implement
    create_wc()
    return {
        'statusCode': 200,
        'body': json.dumps('Tweet with Success using AWS Lambda!')
    }

def remove_hashtag_and_mention(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def create_wc():
    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    keyword = '#BBB22 OR #bbb22'
    n_tweets = 1000

    tweet_list = []

    # datetime object containing current date and time
    tz = pytz.timezone('America/Sao_Paulo')
    ct = datetime.now(tz=tz)
    dt_string = ct.strftime("%d/%m/%Y %H:%M:%S")
    # logger.info("Getting tweets")
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang='pt',tweet_mode="extended").items(n_tweets):
        tweet_list.append(unidecode(tweet.full_text))
    # #cleaning tweets
    tw_list = pd.DataFrame(tweet_list)
    tw_list.drop_duplicates(inplace=True)
    tw_list['original'] = tw_list[0]
    tw_list['text'] = tw_list[0]

    # Lowercase
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

    # Remove hashtag and mention
    tw_list['text'] = tw_list['text'].apply(lambda x: remove_hashtag_and_mention(x))

    # Remove stopwords
    tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([x.strip() for x in x.split() if x not in stopwords]))

    #remove punctuation
    table = str.maketrans('', '', string.punctuation)
    tw_list['text'] = tw_list['text'].apply(lambda x: ' '.join([x.translate(table) for x in x.split()]))

    # create a wordcloud
    # logger.info("Generating WC")
    wc = WordCloud(background_color='white',
                   collocations=False,
                   width=1600,
                   height=800,
                   contour_width=3,
                   contour_color='black',
                   stopwords=stopwords).generate(tw_list['text'].str.cat(sep=' '))
    plt.figure( figsize=(20 ,10), facecolor='k')
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    response = api.media_upload(filename="wordcloud", file=buf)

    status = 'BBB EM: ' + dt_string + ' #BBB22 #bbb22'
    api.update_status(status = status ,media_ids=[response.media_id_string])



