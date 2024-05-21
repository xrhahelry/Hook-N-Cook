from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

# Set up the Chrome driver service
service = Service(executable_path="data/scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Read the CSV file
df = pd.read_csv("data/laptop.csv")

# Extract required columns
urls = df["url"]
cpu_cores = df["cpu cores"]
names = df["name"]

details_list = []

# Loop through each URL
for i, (link, cpu_core, name) in enumerate(zip(urls, cpu_cores, names)):
    driver.get(link)
    details = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_detail"]/div/div[1]/div[1]/ul'))
        )
        detail = driver.find_element(By.XPATH, '//*[@id="module_product_detail"]/div/div[1]/div[1]/ul').text
        details.append(detail)
    except Exception as e:
        # If any exception occurs, print the URL and save it to a failed list
        print(f"Failed to retrieve details for URL: {link}, error: {e}")
        details.append('')
        failed_df = pd.DataFrame([[link]], columns=['url'])
        failed_df.to_csv('failed.csv', mode='a', header=not os.path.exists('failed.csv'), index=False)
    
    # Append name, cpu_cores, and url to the details
    details.append(name)
    details.append(cpu_core)
    details.append(link)
    
    details_list.append(details)

    # Print the current details list for debugging
    print(details)
    time.sleep(1)

# Create a DataFrame from the details list with appropriate column names
details_df = pd.DataFrame(details_list, columns=['details', 'name', 'cpu_cores', 'url'])

# Save the DataFrame to CSV
details_df.to_csv('detailed_df.csv', index=False)

# Quit the driver
driver.quit()
