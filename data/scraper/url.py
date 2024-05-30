import hashlib

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def url_scraper(driver):
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
