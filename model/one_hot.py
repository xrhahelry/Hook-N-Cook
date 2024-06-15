import numpy as np
import pandas as pd


def one_hot(selected_item, limit, sort, num):
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
        "graphics card",
    ]

    df = laptops[reorder]

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

    selected_item["price"] = int((((selected_item["price"] - min) / (max - min)) * 100))
    new_df = pd.DataFrame([selected_item])
    new_df_enc = pd.get_dummies(new_df, columns=categorical_cols)
    new_df_enc = new_df_enc.reindex(columns=df_enc.columns, fill_value=0)
    for col in one_hot_cols:
        new_df_enc[col] = new_df_enc[col].apply(lambda x: int(x))

    enc = df_enc.set_index("id")
    not_enc = laptops.set_index("id")
    new_enc = new_df_enc.set_index("id")

    vector1 = new_enc.loc["00000", :].to_numpy()[2:]

    for id, data in enc.iterrows():
        vector2 = enc.loc[id, :].to_numpy()[2:]
        distance = np.linalg.norm(vector1 - vector2)

        if distance <= limit:
            product = not_enc.loc[id, :].to_dict()
            product["id"] = id
            product["distance"] = distance
            if product["instock"] == "yes":
                recomm.append(product)

    recomm = sorted(recomm, key=lambda x: x[sort])
    if num == -1:
        return recomm
    else:
        return recomm[:num]
