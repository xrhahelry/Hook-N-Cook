from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
import hashlib

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

# This path works with vscode's code runner plugin.
# If you get an error try just chromedriver
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


def generate_filename(url):
    hashed_url = hashlib.sha256(url.encode()).hexdigest()
    truncated_hash = hashed_url[:10]
    return truncated_hash


files = [generate_filename(url) for url in links]
files = [files[i - 1] + "_" + str(i) + ".csv" for i in range(1, len(files) + 1)]

df = pd.DataFrame(list(zip(links, files)), columns=["Url", "Filename"])

# This path works with vscode's code runner plugin.
# try ../datasets/{filename}.csv if you are running the file from inside the scraper folder
df.to_csv("./datasets/urls_and_filenames.csv", index=False)

driver.quit()
