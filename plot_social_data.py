import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('social_data_2022_03_13.xlsx.csv')
print(data.loc[:,['alias','sentiment','score']])
# data.set_index('Unnamed: 0', inplace=True)
# data.T.plot()
# plt.tight_layout()
# plt.show()