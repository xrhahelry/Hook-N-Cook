from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

query = input("What to look for: ")
info = []

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://daraz.com.np")

WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "q")))

input_element = driver.find_element(By.ID, "q")
input_element.clear()
input_element.send_keys(str(query) + Keys.ENTER)

WebDriverWait(driver, 1).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            '//*[@id="root"]',
        )
    )
)

try:
    images = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[4]/div/div/div[1]'
    ).find_elements(By.TAG_NAME, "img")
except:
    images = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div[1]/div[2]'
    ).find_elements(By.TAG_NAME, "img")

titles = driver.find_elements(By.XPATH, '//*[@id="id-title"]')
prices = driver.find_elements(By.XPATH, '//*[@id="id-price"]/div/div[1]/span[2]')

count = 1
for i in range(0, 20):
    images[i].screenshot("images/" + query + str(count) + ".png")
    info.append([titles[i].text, prices[i].text])
    count += 1

for a in info:
    for b in a:
        print(b)

driver.quit()
