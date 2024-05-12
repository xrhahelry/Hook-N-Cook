from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
import hashlib

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

service = Service(executable_path="./scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

links = []
for i in range(1, 42):
    url = f"https://www.daraz.com.np/laptops/?page={i}"
    driver.get(url)
    time.sleep(1)
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
df.to_csv("./datasets/urls.csv", index=False)

driver.quit()
