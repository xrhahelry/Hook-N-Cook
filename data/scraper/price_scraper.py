from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import date
import os
import hashlib

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

service = Service(executable_path="data/scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
# 1512
# ddf16c064a,82999.0,dell,lnspiron 15,Intel Core i5,8,15.6,512,Not Specified,,,,0.0,0,"Dell lnspiron 15 3511 i5-8GB-512GB-15.6""FHD",https://www.daraz.com.np/products/dell-lnspiron-15-3511-i5-8gb-512gb-156fhd-i120634311-s1032895976.html?search=1
links = []
for i in range(0, 42):
    url = f"https://www.daraz.com.np/laptops/?page={i}"
    driver.get(url)
    products = driver.find_elements(By.XPATH, '//*[@id="id-a-link"]')
    urls = [x.get_property("href") for x in products]
    links += urls


def generate_filename(url):
    hashed_url = hashlib.sha256(url.encode()).hexdigest()
    truncated_url = hashed_url[:10]
    return truncated_url


files = [generate_filename(url) for url in links]
files = [file + ".csv" for file in files]

df = pd.DataFrame(list(zip(links, files)), columns=["Url", "Filename"])
df.drop_duplicates(inplace=True)
df.to_csv("data/scraper/urls.csv", index=False)

today = date.today()

for i in range(0, len(links)):
    print(i)
    if (
        links[i]
        == "https://www.daraz.com.np/products/dell-vostro-3888-computer-set-i114454487-s1031087096.html?search=1"
    ):
        continue

    filename = "data/prices/" + files[i]
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
            "data/scraper/failed.csv",
            header=not os.path.exists("data/scraper/failed.csv"),
            mode="a",
            index=False,
        )
        df = pd.DataFrame(
            [[today, None, None]],
            columns=["Date", "Actual Price", "Discount Price"],
        )

    df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)

driver.delete_all_cookies()
driver.quit()
