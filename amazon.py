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

driver.get("https://amazon.com")

WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id="twotabsearchtextbox"]")))

input_element = driver.find_element(By.ID, "//*[@id="twotabsearchtextbox"]")
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

images = driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/span/div/div/div[1]/span/a/div/img')
titles = driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/span/div/div/div[2]/div[1]/h2/a/span/text()')
prices = driver.find_elements(By.XPATH, '')

count = 1
for i in range(0, 20):
    images[i].screenshot("images/" + query + str(count) + ".png")
    info.append([titles[i].text, prices[i].text])
    count += 1

for a in info:
    for b in a:
        print(b)

driver.quit()
