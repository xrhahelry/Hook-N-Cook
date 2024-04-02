import time

t = time.time()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# query = input("What to look for: ")
query = "laptop"
info = []

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

driver.get("https://daraz.com.np")

input_element = driver.find_element(By.ID, "q")
input_element.clear()
input_element.send_keys(str(query) + Keys.ENTER)

search_results = driver.find_elements(By.XPATH, '//*[@id="id-a-link"]')
urls = [x.get_property("href") for x in search_results]
for url in urls:
    details = []
    details.append(url)
    driver.get(url)
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="J_breadcrumb"]/li[1]/span/a/span',
            )
        )
    )
    category = driver.find_element(
        By.XPATH, '//*[@id="J_breadcrumb"]/li[1]/span/a/span'
    )
    details.append(category.text)
    sub_category = driver.find_element(
        By.XPATH, '//*[@id="J_breadcrumb"]/li[2]/span/a/span'
    )
    details.append(sub_category.text)
    type = driver.find_element(By.XPATH, '//*[@id="J_breadcrumb"]/li[3]/span/a/span')
    details.append(type.text)
    name = driver.find_element(
        By.XPATH, '//*[@id="module_product_title_1"]/div/div/span'
    )
    details.append(name.text)
    try:
        actual_price = driver.find_element(
            By.XPATH, '//*[@id="module_product_price_1"]/div/div/div/span[1]'
        )
        details.append(actual_price.text)
        discount_price = driver.find_element(
            By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
        )
        details.append(discount_price.text)
    except:
        actual_price = driver.find_element(
            By.XPATH, '//*[@id="module_product_price_1"]/div/div/span'
        )
        details.append(actual_price.text)
        details.append(actual_price.text)
    driver.execute_script("window.scrollTo(0, 300)")
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[1]/span[1]',
            )
        )
    )
    score = driver.find_element(
        By.XPATH,
        '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[1]/span[1]',
    )
    details.append(score.text)
    reviews = driver.find_element(
        By.XPATH, '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[3]'
    )
    details.append(reviews.text)
    print(details)
    print(" ")

driver.quit()


print("time taken: ", time.time() - t)
