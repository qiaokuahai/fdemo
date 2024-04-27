import pandas as pd
import numpy as np

data1 =[
    {
      "id": "A001",
      "name": "菜鸟教程",
      "url": "www.runoob.com",
      "likes": 61
    },
    {
      "id": "A002",
      "name": "Google",
      "url": "www.google.com",
      "likes": 124
    },
    {
      "id": "A003",
      "name": "淘宝",
      "url": "www.taobao.com",
      "likes": 45
    }
]
df1 = pd.DataFrame(data1)

# print(df1)

data2 =[
    {
      "id": "A001",
      "name": "java",
      "url": "www.java.com",
      "likes": 90
    },
    {
      "id": "A002",
      "name": "python",
      "url": "www.python.com",
      "likes": 91
    },
    {
      "id": "A006",
      "name": "golang",
      "url": "www.golang.com",
      "likes": 92
    }
]
df2 = pd.DataFrame(data2)

# print(df2)

df1.set_index("id", inplace=True)
df2.set_index("id", inplace=True)

df1.columns = pd.MultiIndex.from_tuples([('one', 'name'), ('one', 'url'), ('one', 'likes')])
df2.columns = pd.MultiIndex.from_tuples([('two', 'name'), ('two', 'url'), ('two', 'likes')])
df3 = pd.concat([df1, df2], axis=1)
# print("=================")
df3.dropna(axis=0, inplace=True)
print(df3)
# print(df1)
# res = df1[['name', 'likes']].groupby('name').agg({"likes": 'mean'})
# res = df1.groupby('name').agg({"likes": 'mean'})

# print(res)

