import pandas as pd

unclean_data = pd.read_csv("data/laptop.csv")

non_categorical_cols = ["id", "price", "brand", "model"]
categorical_cols = ["processor", "ram memory", "display size", "storage capacity"]

df = unclean_data[non_categorical_cols + categorical_cols]

df_enc = pd.get_dummies(df, columns=categorical_cols)

cols = df_enc.columns.to_list()
one_hot_cols = list(set(cols) - set(non_categorical_cols))

for col in one_hot_cols:
    df_enc[col] = df_enc[col].apply(lambda x: int(x))

df_enc.to_csv("model/one_hot_encoded_data.csv", index=False)
