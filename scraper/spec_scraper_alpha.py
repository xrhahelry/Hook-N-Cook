from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

service = Service(executable_path="./scraper/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

df = pd.read_csv("../datasets/urls.csv")
links = df["Url"]
file = df["Filename"]
titles = []
for x in range(len(links)):
    data = []
    driver.get(links[x])

    driver.execute_script("window.scrollTo(0, 300)")
    try:
        view = driver.find_element(
            By.XPATH, '//*[@id="module_product_detail"]/div/div[2]/button'
        )
        driver.execute_script("arguments[0].scrollIntoView();", view)
        driver.execute_script("window.scrollBy(0, -100)")
        view.click()
        specs = driver.find_element(
            By.XPATH, '//*[@id="module_product_detail"]/div/div[1]/div[3]/h2'
        )
        driver.execute_script("arguments[0].scrollIntoView();", specs)
        driver.execute_script("window.scrollBy(0, -100)")
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="module_product_detail"]/div/div/div[3]/div[1]/ul',
                )
            )
        )
        stitle = driver.find_elements(By.CLASS_NAME, "key-title")
    except:
        try:
            specs = driver.find_element(
                By.XPATH, '//*[@id="module_product_detail"]/div/div/div[3]/h2'
            )
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="module_product_detail"]/div/div/div[3]/div[1]/ul',
                    )
                )
            )
            stitle = driver.find_elements(By.CLASS_NAME, "key-title")
        except:
            specs = driver.find_element(
                By.XPATH, '//*[@id="module_product_detail"]/div/div/div[2]/h2'
            )
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="module_product_detail"]/div/div/div[2]/div[1]/ul',
                    )
                )
            )
            stitle = driver.find_elements(By.CLASS_NAME, "key-title")

    titles += data
    data = [x.text for x in stitle]
    print(data)

filepath = "./datasets/" + "titles.csv"
df = pd.DataFrame(titles, columns=['Title'])
df.to_csv(filepath, index=False)

driver.delete_all_cookies()
driver.quit()
