import numpy as np
import pandas as pd

df_enc = pd.read_csv("model/1ton_encoded_data.csv")
df = pd.read_csv("data/laptop.csv")
enc = df_enc.set_index("id")
not_enc = df.set_index("id")

choice = "012a16c221"
vector1 = enc.loc[choice, :].to_numpy()[2:]
list1 = not_enc.loc[choice, :].tolist()[:-2]


for id, data in enc.iterrows():
    if id == choice:
        continue
    vector2 = enc.loc[id, :].to_numpy()[2:]
    distance = np.linalg.norm(vector1 - vector2)
    if distance <= 3:
        list2 = not_enc.loc[id, :].tolist()[:-2]
        print(distance)
        print(list1)
        print(list2)
        print("===========")