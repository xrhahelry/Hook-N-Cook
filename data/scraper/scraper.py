import price
import specs
import url
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

service = Service(executable_path="data/scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)


def main():
    # url.url_scraper(driver)
    # price.price_scraper(driver)
    specs.specs_scraper(driver)


if __name__ == "__main__":
    main()

driver.delete_all_cookies()
driver.quit()
