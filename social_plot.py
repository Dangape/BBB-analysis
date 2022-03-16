import boto3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def read_s3_csv(bucket, file_path):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=file_path)
    df = pd.read_csv(obj['Body'])
    return df

bucket = 'tweet-bot-data'
file_path = 'social_data/social_data.csv'

df = read_s3_csv(bucket,file_path)
df['score'] = df['score']/1000
# df.plot(x='alias',y='score',kind='bar')
# sns.set_style("whitegrid")
# sns.barplot(data=df,x='alias',y='score')
# sns.despine()
# plt.title('Engajamento - Twitter (Relativo a número de seguidores)')
# plt.tight_layout()
# plt.show()

fg = sns.FacetGrid(data=df, hue='alias', aspect=1.61)
fg.map(plt.plot, 'date', 'score').add_legend()
plt.show()