import pandas as pd
import matplotlib.pyplot as plt
from config import create_api
import pytz
from datetime import datetime
import tweepy
from unidecode import unidecode
import json
import io
import time
import boto3
from dateutil import tz as timezone

start_time = time.time()
def handler(event, context):
    create_paredao_plot()
    return {
        'statusCode': 200,
        'body': json.dumps('Tweet with Success using AWS Lambda!')
    }

def create_paredao_plot():
    api = create_api()
    paredao = ['#forajessi', '#foraeli', '#foraeliezer', '#foraeslo', '#foraeslovenia', '#foravyni', '#foraviny',
               '#forapa', '#forapauloandre', '#foradg', '#foradouglas', '#foradouglassilva', '#foraarthur',
               '#forarrthur','#foralina', '#foralinn', '#foralinna', '#foralucas', '#forabarao', '#foranatalia',
               '#foragustavo', '#foralais', '#forascooby']

    # datetime object containing current date and tim
    tz = pytz.timezone('America/Sao_Paulo')
    ct = datetime.now(tz=tz)
    dt_string = ct.strftime("%d/%m/%Y %H:%M:%S")

    def convert_utc(row):
        from_zone = timezone.gettz('UTC')
        to_zone = timezone.gettz('America/Sao_Paulo')
        utc = datetime.strptime( row['created_at'], "%d/%m/%Y %H:%M:%S")
        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
        return  central.strftime("%d/%m/%Y %H:%M:%S")

    def read_s3_csv(bucket, file_path):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=file_path)
        df = pd.read_csv(obj['Body'])
        return df

    bucket = 'tweet-bot-data'
    file_path = 'social_data/paredao.csv'

    df = read_s3_csv(bucket, file_path)
    df['created_at'] = df.apply(lambda x: convert_utc(x), axis=1)
    df['paredao'].fillna('', inplace=True)

    # treat similar names
    df['paredao'] = df['paredao'].apply(lambda x: ' '.join([word.replace('viny', 'vyni') for word in x.split()]))
    df['paredao'] = df['paredao'].apply(lambda x: ' '.join([word.replace('eslovenia', 'eslo') for word in x.split()]))

    print(df.loc[:,['created_at','updated_at']])
    df = pd.DataFrame(df[df['paredao'] != '']['paredao'].value_counts(normalize=True).sort_values(ascending=False))
    df['paredao'] = df['paredao'] * 100
    df = df.iloc[:3, :]
    # print(df)

    plt.rcdefaults()
    fig, ax = plt.subplots()
    bars = ax.bar(
        x=df.index,
        height=df.paredao,
        tick_label=df.index)

    # Axis formatting.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    # Grab the color of the bars so we can make the
    # text the same color.
    # bar_color = bars[0].get_facecolor()
    # Add text annotations to the top of the bars.
    # Note, you'll have to adjust this slightly (the 0.3)
    # with different data.

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.6,
            str(round(bar.get_height(), 2)) + '%',
            horizontalalignment='center',
            color='black',
            weight='bold'
        )

    # Add labels and a title. Note the use of `labelpad` and `pad` to add some
    # extra space between the text and the tick labels.
    ax.set_xlabel('Hashtags', labelpad=15, color='#333333')
    ax.set_ylabel('%', labelpad=15, color='#333333')
    ax.set_title('Termômetro dos emparedados no twitter', pad=15, color='#333333',
                 weight='bold')
    # plt.xticks(rotation=80)

    # Make the chart fill out the figure better.
    fig.tight_layout()
    plt.savefig('paredao.png')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    # response = api.media_upload(filename="paredao", file=buf)
    #
    # status = 'PAREDÃO BBB EM: ' + dt_string + ' #BBB22 #bbb22'
    # api.update_status(status=status, media_ids=[response.media_id_string])

create_paredao_plot()

print("--- %s minutes ---" % ((time.time() - start_time)/60))