from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import os
import re
from datetime import date
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

urls = pd.read_csv("../datasets/laptops_url_dataset.csv")
links = urls["Url"]

failed = []
for link in links:
    driver.get(link)
    try:
        actual_price = driver.find_element(
            By.XPATH, '//*[@id="module_product_price_1"]/div/div/div/span[1]'
        ).text

        discount_price = driver.find_element(
            By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
        ).text
    except:
        actual_price = driver.find_element(
            By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
        ).text

        discount_price = actual_price

    today = date.today()
    df = pd.DataFrame(
        [[today, actual_price, discount_price]],
        columns=["Date", "Actual Price", "Discount Price"],
    )
    df["Actual Price"] = df["Actual Price"].str.replace("Rs. ", "").str.replace(",", "")
    df["Discount Price"] = (
        df["Discount Price"].str.replace("Rs. ", "").str.replace(",", "")
    )
    name = str(link)
    name = re.sub(r"[^a-zA-Z0-9]", "", name)
    name = re.sub(r"httpswwwdarazcomnpproducts", "", name)
    filename = "../datasets/prices/" + name + ".csv"
    df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
    time.sleep(1)
