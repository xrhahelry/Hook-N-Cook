import pandas as pd

unclean_data = pd.read_csv("data/laptop.csv")

non_categorical_cols = ["id", "price", "brand", "model"]
categorical_cols = ["processor", "ram memory", "display size", "storage capacity"]
reorder = [
    "id",
    "brand",
    "model",
    "price",
    "processor",
    "ram memory",
    "display size",
    "storage capacity",
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

df_enc.to_csv("model/one_hot_encoded_data.csv", index=False)
