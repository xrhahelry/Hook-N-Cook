import numpy as np
import pandas as pd


def one_n(selected_item, limit):
    laptops = pd.read_csv("data/laptop.csv")
    recomm = []
    non_categorical_cols = ["id", "price", "brand", "model"]
    categorical_cols = [
        "processor",
        "ram memory",
        "display size",
        "storage capacity",
        "cpu cores",
        "graphics card",
    ]

    df = laptops[non_categorical_cols + categorical_cols]

    encoder_rules = {key: "" for key in categorical_cols}
    for col in categorical_cols:
        unique_values = df[col].unique().tolist()
        unique_values = sorted(unique_values)
        encoder_rules[col] = {
            value: index + 1 for index, value in enumerate(unique_values)
        }

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
            "graphics card",
        ]
    ]

    enc_rules = {
        "processor": {
            "2": 1,
            "3": 2,
            "5": 3,
            "6.5": 4,
            "7": 5,
            "7.5": 6,
            "8.5": 7,
            "9": 8,
        },
        "ram memory": {"4": 1, "6": 2, "8": 3, "12": 4, "16": 5, "24": 6, "32": 7},
        "display size": {
            "10.5": 1,
            "11.6": 2,
            "12.0": 3,
            "13.3": 4,
            "13.5": 5,
            "13.6": 6,
            "14.0": 7,
            "14.1": 8,
            "14.5": 9,
            "15.0": 10,
            "15.6": 11,
            "16.0": 12,
            "16.1": 13,
            "16.2": 14,
            "17.0": 15,
            "17.3": 16,
        },
        "storage capacity": {
            "64": 1,
            "128": 2,
            "256": 3,
            "512": 4,
            "1024": 5,
            "2048": 6,
        },
        "cpu cores": {
            "1": 1,
            "2": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "8": 6,
            "10": 7,
            "12": 8,
            "14": 9,
            "16": 10,
            "20": 11,
            "24": 12,
        },
        "graphics card": {
            "0": 1,
            "1000": 2,
            "1050": 3,
            "1300": 4,
            "1400": 5,
            "1500": 6,
            "1650": 7,
            "1660": 8,
            "2000": 9,
            "2040": 10,
            "2050": 11,
            "2060": 12,
            "2070": 13,
            "2500": 14,
            "2800": 15,
            "2900": 16,
            "3050": 17,
            "3060": 18,
            "3070": 19,
            "4050": 20,
            "4060": 21,
            "4070": 22,
        },
    }
    selected_item["price"] = int((((selected_item["price"] - min) / (max - min)) * 100))
    new_df = pd.DataFrame([selected_item])
    for key in encoder_rules:
        new_df.loc[:, key] = new_df.loc[:, key].map(enc_rules[key]).astype(int)
    enc = df.set_index("id")
    not_enc = laptops.set_index("id")
    new_enc = new_df.set_index("id")

    vector1 = new_enc.loc["00000", :].to_numpy()[2:]

    if limit == 1:
        limit = 3
    elif limit == 3:
        limit = 4
    elif limit == 8:
        limit = 9

    for id, data in enc.iterrows():
        vector2 = enc.loc[id, :].to_numpy()[2:]
        distance = np.linalg.norm(vector1 - vector2)

        if distance <= limit:
            product = not_enc.loc[id, :].to_dict()
            product["id"] = id
            if product["instock"] == "yes":
                recomm.append(product)

    recomm = sorted(recomm, key=lambda x: x["price"])
    return recomm
