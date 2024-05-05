from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import date
import os
import re

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

service = Service(executable_path="./scraper/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

df = pd.read_csv("../datasets/urls.csv")
links = df["Url"]
file = df["Filename"]

newdf=pd.DataFrame()
for x in range(len(links)):
    
    driver.get(links[x])
    details= []
    urls = str(links[x])
    fn = str(file[x])
    details.append(urls)
    details.append(fn)

    try:
        name = driver.find_element(
            By.XPATH, '//*[@id="module_product_title_1"]/div/div/span'
        ).text
        details.append(name)
        driver.execute_script("window.scrollTo(0, 300)")
    except:
        continue
        
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
    details.append(rating)
    details.append(reviews)

  
    try:
        view = driver.find_element(
            By.XPATH, '//*[@id="module_product_detail"]/div/div[2]/button'
        )
        driver.execute_script("arguments[0].scrollIntoView();",view)
        driver.execute_script("window.scrollBy(0, -100)")
        view.click()
        specs = driver.find_element(
            By.XPATH, '//*[@id="module_product_detail"]/div/div[1]/div[3]/h2'
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

        
  
    details.append(specs_list)
    print(details)
    
    df=pd.DataFrame(
        [[urls, fn, name, rating, reviews, specs_list]], columns=["Urls", "Filename", "Name", "Rating", "Review", "Specification"]
    )
    df["Name"] = (
        df["Name"].str.strip("")
    )

    newdf = pd.concat([newdf, df], ignore_index=True)
    time.sleep(1)


filepath = "../datasets/" + 'ProductDetail2.csv'
newdf.to_csv(filepath, index=False)

driver.quit()
