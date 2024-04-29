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

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

df = pd.read_csv("../datasets/urls.csv")
links = df["Url"]

file = df["Filename"]
today = date.today()


for x in range(1, 1000):
    filename = "../datasets/specs" + file[x]
    driver.get(links[x])

    name = driver.find_element(
        By.XPATH, '//*[@id="module_product_title_1"]/div/div/span'
    ).text

    driver.execute_script("window.scrollTo(0, 300)")
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[1]/span[1]',
                )
            )
        )
        rating = driver.find_element(
            By.XPATH,
            '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[1]/span[1]',
        ).text

        reviews = driver.find_element(
            By.XPATH,
            '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[3]',
        ).text
    except:
        rating = "0"
        reviews = "0"

    try:
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
            specs_list = driver.find_element(
                By.XPATH, '//*[@id="module_product_detail"]/div/div/div[3]/div[1]/ul'
            ).text
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
            specs_list = driver.find_element(
                By.XPATH, '//*[@id="module_product_detail"]/div/div/div[2]/div[1]/ul'
            ).text

    except:
        view = driver.find_element(
            By.XPATH, '//*[@id="module_product_detail"]/div/div[2]/button'
        )
        driver.execute_script("arguments[0].scrollIntoView();",view)
        view.click()
        specs = driver.find_element(
            By.XPATH, '//*[@id="module_product_detail"]/div/div/div[3]/h2'
        )
        driver.execute_script("arguments[0].scrollIntoView();",specs)
        driver.execute_script("window.scrollBy(0, -100)")
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="module_product_detail"]/div/div/div[3]/div[1]/ul',
                )
            )
        )
        specs_list = driver.find_element(
            By.XPATH, '//*[@id="module_product_detail"]/div/div/div[3]/div[1]/ul'
        ).text

    df = pd.DataFrame(
        [[today, name, rating, reviews, specs_list]],
        columns = ["Date", "Name", "Rating", "Reviews", "Specification"]
    )

    df.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)
    time.sleep(1)

driver.quit()
