import pandas as pd

laptop = pd.read_csv("data/laptop.csv")

print(laptop.info())

laptop = laptop.drop(columns=["graphics memory"])
laptop.to_csv("data/lap.csv", index=False)

# def clean_processor(processor):
#     if "7" in processor:
#         return "7"
#     elif "5" in processor:
#         return "5"
#     elif "3" in processor:
#         return "3"
#     elif "9" in processor:
#         return "9"
#     elif "celeron" in processor.lower():
#         return "2"
#     elif "m1" in processor.lower():
#         return "6.5"
#     elif "m2" in processor.lower():
#         return "7.5"
#     else:
#         return processor


# laptop["price"] = laptop["price"].apply(lambda x: int(x))
# laptop["cpu cores"] = laptop["cpu cores"].apply(lambda x: int(x))
# laptop["name"] = laptop["name"].apply(lambda x: str(x))
# laptop["brand"] = laptop["brand"].apply(lambda x: str(x))
# laptop.loc[laptop["ram memory"] == "1", "ram memory"] = "16"
# laptop.loc[laptop["ram memory"] == "3", "ram memory"] = "4"
# laptop.loc[laptop["ram memory"] == "Not Specified", "ram memory"] = "8"
# laptop.loc[laptop["ram memory"].isna(), "ram memory"] = "8"
# laptop["ram memory"] = laptop["ram memory"].apply(lambda x: int(x))
# laptop["display size"] = laptop["display size"].apply(lambda x: float(x))
# laptop["processor"] = laptop["processor"].apply(clean_processor)

# temp = laptop[['processor', 'name', 'url']]
# temp.to_csv('temp.csv', index=False)
# tempp = pd.read_csv("temp.csv")
# tempp['processor'].value_counts()
# laptop['processor'] = tempp['processor'].astype(float)
# print(laptop.info())
# laptop.to_csv("data/laptop.csv", index=False)
