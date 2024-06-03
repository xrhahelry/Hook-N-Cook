import numpy as np
import pandas as pd

unclean_data = pd.read_csv("data/laptop.csv")

non_categorical_cols = ["id", "price", "brand", "model"]
categorical_cols = [
    "processor",
    "ram memory",
    "display size",
    "storage capacity",
    "cpu cores",
]
reorder = [
    "id",
    "brand",
    "model",
    "price",
    "processor",
    "ram memory",
    "display size",
    "storage capacity",
    "cpu cores",
]

df = unclean_data[reorder]

df_enc = pd.get_dummies(df, columns=categorical_cols)

cols = df_enc.columns.to_list()
one_hot_cols = list(set(cols) - set(non_categorical_cols))

for col in one_hot_cols:
    df_enc[col] = df_enc[col].apply(lambda x: int(x))

max = df_enc["price"].max()
min = df_enc["price"].min()
df_enc["price"] = df_enc["price"].apply(lambda x: (x - min) / (max - min))
df_enc["price"] = df_enc["price"].apply(lambda x: x * 100)
df_enc["price"] = df_enc["price"].astype(float).astype(int)

enc = df_enc.set_index("id")
not_enc = df.set_index("id")

choice = "012a16c221"
vector1 = enc.loc[choice, :].to_numpy()[2:]
list1 = not_enc.loc[choice, :].tolist()

for id, data in enc.iterrows():
    if id == choice:
        continue
    vector2 = enc.loc[id, :].to_numpy()[2:]
    distance = np.linalg.norm(vector1 - vector2)

    if distance <= 3:
        list2 = not_enc.loc[id, :].tolist()
        print(distance)
        print(list1)
        print(list2)
        print("===========")
