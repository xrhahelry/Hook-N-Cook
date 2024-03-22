from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://daraz.com.np")

input_element = driver.find_element(By.ID, "q")
input_element.send_keys("smartwatch" + Keys.ENTER)

driver.quit()