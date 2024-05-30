import hashlib
import os
import re
from datetime import date

import pandas as pd
import price
import specs
import url
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


def main():
    url.url_scraper()
    price.price_scraper()
    specs.specs_scraper()


if __name__ == "__main__":
    main()

driver.delete_all_cookies()
driver.quit()
