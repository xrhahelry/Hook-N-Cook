from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import date
import os

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

service = Service(executable_path="scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

df = pd.read_csv("./datasets/urls.csv")
links = df["Url"]
files = df["Filename"]
today = date.today()

for i in range(0, len(links)):
    print(i)
    filename = "./datasets/prices/" + files[i]
    driver.get(links[i])
    try:
        try:
            actual_price = driver.find_element(
                By.XPATH, '//*[@id="module_product_price_1"]/div/div/div/span[1]'
            ).text

            discount_price = driver.find_element(
                By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
            ).text
        except:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="module_product_price_1"]/div/div/span',
                    )
                )
            )
            actual_price = driver.find_element(
                By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
            ).text

            discount_price = actual_price

        df = pd.DataFrame(
            [[today, actual_price, discount_price]],
            columns=["Date", "Actual Price", "Discount Price"],
        )
        df["Actual Price"] = (
            df["Actual Price"].str.replace("Rs. ", "").str.replace(",", "")
        )
        df["Discount Price"] = (
            df["Discount Price"].str.replace("Rs. ", "").str.replace(",", "")
        )
    except:
        print(links[i])
        dd = pd.DataFrame([[files[i], links[i]]], columns=["Filename", "Url"])
        dd.to_csv(
            "./datasets/failed.csv",
            header=not os.path.exists("./datasets/failed.csv"),
            mode="a",
            index=False,
        )
        df = pd.DataFrame(
            [[today, None, None]],
            columns=["Date", "Actual Price", "Discount Price"],
        )

    df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
    time.sleep(1)

driver.delete_all_cookies()
driver.quit()
