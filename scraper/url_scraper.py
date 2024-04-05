from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

service = Service(executable_path="./scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.daraz.com.np/laptops/")

links = []
for i in range(0, 41):
    products = driver.find_elements(By.XPATH, '//*[@id="id-a-link"]')
    urls = [x.get_property("href") for x in products]
    links += urls
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
    next = driver.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[3]/div[2]/div/ul/li[9]/a',
    )
    next.click()
    time.sleep(1)

df = pd.DataFrame(links, columns=["Url"])
df.drop_duplicates()
df.to_csv("./datasets/laptops_url_dataset1.csv", index=False)

driver.quit()
