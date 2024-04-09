import pandas as pd

df = pd.read_csv("./datasets/laptops_url_dataset.csv")
chunk_size = 820
split = [df[x : x + chunk_size] for x in range(0, len(df), chunk_size)]

split[0].to_csv("./datasets/sujal.csv", index=False)
split[1].to_csv("./datasets/yajjyu.csv", index=False)
