import pandas as pd
import matplotlib.pyplot as plt
from config import create_api
import pytz
from datetime import datetime
import tweepy
from unidecode import unidecode
import json
import io

#
# data = pd.read_csv('social_data_2022_03_13.xlsx.csv')
# print(data.loc[:,['alias','sentiment','score']])
# data.set_index('Unnamed: 0', inplace=True)
# data.T.plot()
# plt.tight_layout()
# plt.show()

# def handler(event, context):
#     # TODO implement
#     create_paredao_plot()
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Tweet with Success using AWS Lambda!')
#     }

def create_paredao_plot(keyword,n_tweets):
    api = create_api()
    tweet_list = []

    paredao = ['#forajessi', '#foraeli', '#foraeliezer', '#foraeslo', '#foraeslovenia', '#foravyni', '#foraviny',
               '#forapa', '#forapauloandre', '#foradg', '#foradouglas', '#foradouglassilva', '#foraarthur',
               '#forarrthur','#foralina', '#foralinn', '#foralinna', '#foralucas', '#forabarao', '#foranatalia',
               '#foragustavo', '#foralais', '#forascooby']

    # datetime object containing current date and time
    tz = pytz.timezone('America/Sao_Paulo')
    ct = datetime.now(tz=tz)
    dt_string = ct.strftime("%d/%m/%Y %H:%M:%S")

    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang='pt',tweet_mode="extended").items(n_tweets):
        tweet_list.append(unidecode(tweet.full_text))

    tw_list = pd.DataFrame(tweet_list)
    tw_list.drop_duplicates(inplace=True)
    tw_list['original'] = tw_list[0]

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

    plt.figure(figsize=(20, 10))
    tw_list.paredao.value_counts().sort_values().plot(kind='barh')
    plt.tight_layout()
    plt.savefig('paredao.png')
    # buf = io.BytesIO()
    # plt.savefig(buf, format='png')
    # buf.seek(0)
    # response = api.media_upload(filename="wordcloud", file=buf)

    # status = 'BBB EM: ' + dt_string + ' #BBB22 #bbb22'
    # api.update_status(status=status, media_ids=[response.media_id_string])

create_paredao_plot('#ForaScooby OR #ForaVyni OR #ForaViny OR #ForaGustavo',5000)