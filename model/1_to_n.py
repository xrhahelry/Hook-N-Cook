import numpy as np
import pandas as pd

laptops = pd.read_csv("data/laptop.csv")

non_categorical_cols = ["id", "price", "brand", "model"]
categorical_cols = [
    "processor",
    "ram memory",
    "display size",
    "storage capacity",
    "cpu cores",
]

df = laptops[non_categorical_cols + categorical_cols]

encoder_rules = {key: "" for key in categorical_cols}
for col in categorical_cols:
    unique_values = df[col].unique().tolist()
    unique_values = sorted(unique_values)
    encoder_rules[col] = {value: index + 1 for index, value in enumerate(unique_values)}

for key in encoder_rules:
    df.loc[:, key] = df.loc[:, key].map(encoder_rules[key]).astype(int)

df["price"] = df["price"].astype(float)
max = df["price"].max()
min = df["price"].min()
df.loc[:, "price"] = (df.loc[:, "price"] - min) / (max - min)
df.loc[:, "price"] = (df.loc[:, "price"] * 100).astype(int)
df = df[
    [
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
]

enc = df.set_index("id")
not_enc = laptops.set_index("id")

choice = "5bffcd46c3"
vector1 = enc.loc[choice, :].to_numpy()[2:]
list1 = not_enc.loc[choice, :].tolist()[:-4]


for id, data in enc.iterrows():
    if id == choice:
        continue
    vector2 = enc.loc[id, :].to_numpy()[2:]
    distance = np.linalg.norm(vector1 - vector2)
    if distance <= 3:
        list2 = not_enc.loc[id, :].tolist()[:-4]
        print(distance)
        print(list1)
        print(list2)
        print("===========")