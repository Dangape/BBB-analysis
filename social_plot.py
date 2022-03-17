import boto3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import pytz


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

sns.set(rc={"figure.figsize":(15, 8)})
sns.set(font_scale=1.5)
sns.set_style("whitegrid")
sns.barplot(data=df[df['date']==dt_string].sort_values(by='score',ascending=False),x='alias',y='score',ci=None).set(title="Score de engajamento no Twitter",ylabel="Score",xlabel=None)
sns.despine()
plt.title('Engajamento nos Últimos 3 Dias (Twitter) - {}'.format(datetime.now(tz=tz).strftime("%d/%m")))
plt.tight_layout()
plt.show()

# sns.set(rc={"figure.figsize":(15, 8)})
# sns.set(font_scale=1.5)
# sns.set_style("white")
# sns.lineplot(
#     data=df,
#     x="date", y="score", hue="alias",marker='o',palette=sns.color_palette('Paired', n_colors=len(np.unique(df.alias)))).\
#     set(title="Score de engajamento no Twitter",ylabel="Score",
#     xlabel=None)
#
# plt.legend(loc='upper right',bbox_to_anchor=(1.25, 1),title='Participantes',borderaxespad=0)
# plt.tight_layout()
# plt.show()