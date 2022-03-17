import boto3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import pytz
from config import create_api
import io
import json

def handler(event, context):
    engagement_plot()
    return {
        'statusCode': 200,
        'body': json.dumps('Tweet with Success using AWS Lambda!')
    }

def engagement_plot():

    def read_s3_csv(bucket, file_path):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=file_path)
        df = pd.read_csv(obj['Body'])
        return df

    bucket = 'tweet-bot-data'
    file_path = 'social_data/social_data.csv'

    tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(tz=tz)
    dt_string = today.strftime("%Y-%m-%d")

    df = read_s3_csv(bucket,file_path)
    df = df[df['alias'] != 'vyni'] #eliminado
    df['score'] = df['score']/100

    df['format_date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m')

    api = create_api()
    participantes = np.unique(df['alias'])
    palette = sns.color_palette('Paired',n_colors=len(np.unique(df.alias)))
    palette_dict = {continent: color for continent, color in zip(participantes, palette)}

    #Barplot
    fig1 = plt.figure(figsize=(15, 8))
    # sns.set(rc={"figure.figsize":(15, 8)})
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    sns.barplot(data=df[df['date']==dt_string].sort_values(by='score',ascending=False),
                x='alias',y='score',ci=None,palette=palette_dict)\
        .set(title="Score de engajamento no Twitter",ylabel="Score",xlabel=None)
    sns.despine()
    plt.title('Engajamento nos Últimos 3 Dias (Twitter) - Referência: {}'.format(datetime.now(tz=tz).strftime("%d/%m")))
    plt.tight_layout()

    #Save barplot
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    # plt.show()

    #lineplot
    fig2 = plt.figure(figsize=(15, 8))
    # sns.set(rc={"figure.figsize":(15, 8)})
    sns.set(font_scale=1.5)
    sns.set_style("white")
    sns.lineplot(
        data=df,
        x="format_date", y="score", hue="alias",marker='o', linewidth=2.0,palette=palette_dict).\
        set(title="Histórico de Engajamento no Twitter",ylabel="Score",
        xlabel=None)
    plt.legend(loc='upper right',bbox_to_anchor=(1.15, 1),title='Participantes',borderaxespad=0)
    sns.despine()
    plt.tight_layout()

    #Save lineplot
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    plt.show()

    response1 = api.media_upload(filename="bar_plot", file=buf1)
    response2 = api.media_upload(filename="line_plot", file=buf2)

    status = 'Engajamento dos perfis oficiais dos participantes do BBB em: ' + dt_string + ' #BBB22 #bbb22'
    api.update_status(status=status, media_ids=[response1.media_id_string,response2.media_id_string])

# engagement_plot()