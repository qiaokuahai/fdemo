import pandas as pd
import numpy as np

data1 = {
    "id": [1, 2, 3, 4, 5],
    "name": ["zhang", "wang", "li", "zhao", "sun"], 
    "score": [91, 92, 93, 95, 90]
}
df1 = pd.DataFrame(data1)
df1.set_index("id", inplace=True)
df1.sort_values("score", inplace=True, ascending=False)
print(df1)
df1.sort_index(ascending=True, inplace=True)
res = df1[df1["score"] > 92]
print(res)
# print(df1)


