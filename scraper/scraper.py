import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
options.add_argument("--headless")

service = Service(executable_path="scraper/geckodriver")

driver = webdriver.Firefox(service=service, options=options)


def main():
    driver.get(
        "https://www.daraz.com.np/products/dell-vostro-3520-i3-12th-gen-16gb-ram-512gb-ssd-156-120hz-fhd-display-laptop-i129017788-s1037011250.html?search=1"
    )

    name = driver.find_element(
        By.XPATH, '//*[@id="module_product_title_1"]/div/div/span'
    ).text
    driver.execute_script("window.scrollBy(0, -300)")
    details = driver.find_element(
        By.XPATH, "/html/body/div[4]/div/div[9]/div[1]/div[2]/div/div/div/div[1]/ul"
    ).text
    specs = driver.find_element(
        By.XPATH,
        "/html/body/div[4]/div/div[9]/div[1]/div[2]/div/div/div/div[3]/div[1]/ul",
    ).text

    with open("data/file.txt", "w") as file:
        file.write(name + " ")
        file.write(details.replace("\n", " "))
        file.write(specs)


if __name__ == "__main__":
    main()

driver.delete_all_cookies()
driver.quit()
