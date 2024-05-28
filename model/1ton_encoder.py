import pandas as pd

unclean_data = pd.read_csv("data/laptop.csv")

non_categorical_cols = ["id", "price", "brand", "model"]
categorical_cols = ["processor", "ram memory", "display size", "storage capacity"]

df = unclean_data[non_categorical_cols + categorical_cols]

encoder_rules = {key: "" for key in categorical_cols}
for col in categorical_cols:
    unique_values = df[col].unique().tolist()
    unique_values = sorted(unique_values)
    encoder_rules[col] = {value: index + 1 for index, value in enumerate(unique_values)}

for key in encoder_rules:
    df[key] = df[key].replace(encoder_rules[key])
    df[key] = df[key].apply(lambda x: int(x))

max = df["price"].max()
min = df["price"].min()
df["price"] = df["price"].apply(lambda x: (x - min) / (max - min))
df["price"] = df["price"].apply(lambda x: x * 100)
df["price"] = df["price"].astype(float).astype(int)
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
    ]
]
df.to_csv("model/1ton_encoded_data.csv", index=False)
