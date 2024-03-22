from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://daraz.com.np")

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "q")))

input_element = driver.find_element(By.ID, "q")
input_element.clear()
input_element.send_keys("smart watch" + Keys.ENTER)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="id-img"]'))
)

img = driver.find_element(By.XPATH, '//*[@id="id-img"]')
img.screenshot("watch.png")

time.sleep(2)

driver.quit()
