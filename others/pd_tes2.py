import pandas as pd
import numpy as np

data1 =[
    {
      "id": "A001",
      "name": "cainiao",
      "url": "www.runoob.com",
      "likes": 61,
      "score": 100
    },
    {
      "id": "A002",
      "name": "google",
      "url": "www.google.com",
      "likes": 124,
      "score": 200
    },
    {
      "id": "A003",
      "name": "taobao",
      "url": "www.taobao.com",
      "likes": 45,
      "score": 300
    },
    {
      "id": "A003",
      "name": "taobao",
      "url": "www.taobao.com",
      "likes": 55,
      "score": 400
    }
]
df1 = pd.DataFrame(data1)
# res = df1[['name', 'likes']].groupby('name').agg({"likes": 'mean'})
# res = df1.groupby('name')[['score', 'likes']].agg('mean')

# def last(df_data):
#     return df_data.iloc[-1, :]

# res1 = df1.groupby('name')[['score', 'likes']]
# print(list(res1))
# res2 = res1.apply(last)
# print(res2)

