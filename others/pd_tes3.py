import pandas as pd
import numpy as np

data1 = {
    "id": [1, 2, 3, 4, 5],
    "name": ["zhang", "wang", "li", "zhao", "sun"], 
    "score": [51, 92, 63, 41, 77],
    "class_id": [1, 3, 3, 2, 1]
}

data2 = {
    "id": [1, 2, 3],
    "class": list("ABC")
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

df3 = df1.merge(df2, left_on="class_id", right_on="id")
df3.rename({"id_x": "new"}, axis=1, inplace=True)
df3["cummax"] = df3["score"].cummax()
df3["maxrtn"] = ((1 - df3["score"]/df3["cummax"]) * 100).round(2).astype("str")

print(df3.dtypes)


# print(df1)
# print(df2)
print("==================")
print(df3)

