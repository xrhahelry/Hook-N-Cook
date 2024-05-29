import hashlib
import os
from datetime import date

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

service = Service(executable_path="data/scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

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

df = pd.read_csv("data/scraper/urls.csv")
files = df["Filename"]
links = df["Url"]
today = date.today()

for i, link in enumerate(links):
    if i < 884:
        continue
    if link in [
        "https://www.daraz.com.np/products/dell-precision-3430-sff-core-i7-8700-32ghz-32gb-ram-512gb-solid-state-drive-windows-11-pro-64bit-renewed-i129855105-s1037690646.html?search=1",
        "https://www.daraz.com.np/products/dell-vostro-3888-computer-set-i114454487-s1031087096.html?search=1",
        "https://www.daraz.com.np/products/dell-tiny-i5-6th-generation-8-gb-ram-256-ssd-with-mouse-keyboard-wifi-dongle-and-mouse-pad-i129272829-s1037294262.html?search=1",
    ]:
        continue

    filename = "data/prices/" + files[i]
    driver.get(link)
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
        print(i, filename)
    except:
        print(i, filename, link)
        pp = pd.read_csv(filename)
        df = pd.DataFrame(
            [[today, int(pp.iloc[-1, -2]), int(pp.iloc[-1, -1])]],
            columns=["Date", "Actual Price", "Discount Price"],
        )

    df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)

driver.delete_all_cookies()
driver.quit()
