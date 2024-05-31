import os
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

service = Service(executable_path="data/scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

df = pd.read_csv("data/scraper/urls.csv")
links = df["Url"]
fn = df["Filename"]
filepath = "data/laptop.csv"
data = pd.read_csv("data/laptop.csv")
old = data["id"].to_list()


def update_specs(row):
    """Put scraped values into the dictionary."""
    title = row["Title"]
    value = row["Value"]
    if title in specs:
        specs[title] = value


for i, link in enumerate(links):
    if link in [
        "https://www.daraz.com.np/products/dell-precision-3430-sff-core-i7-8700-32ghz-32gb-ram-512gb-solid-state-drive-windows-11-pro-64bit-renewed-i129855105-s1037690646.html?search=1",
        "https://www.daraz.com.np/products/dell-vostro-3888-computer-set-i114454487-s1031087096.html?search=1",
        "https://www.daraz.com.np/products/dell-tiny-i5-6th-generation-8-gb-ram-256-ssd-with-mouse-keyboard-wifi-dongle-and-mouse-pad-i129272829-s1037294262.html?search=1",
    ]:
        continue

    if fn[i].replace(".csv", "") in old:
        print(i, "data/prices/" + fn[i])
        pp = pd.read_csv("data/prices/" + fn[i])
        data.loc[data.id == fn[i].replace(".csv", ""), "price"] = int(pp.iloc[-1, -1])
        data.to_csv(filepath, index=False)
    else:
        titles = []
        values = []
        specs = {
            "id": None,
            "price": None,
            "brand": None,
            "model": None,
            "processor": None,
            "ram memory": None,
            "display size": None,
            "storage capacity": None,
            "cpu cores": None,
            "graphics card": None,
            "rating": None,
            "reviews": None,
            "name": None,
            "url": None,
        }
        driver.get(link)
        try:
            name = driver.find_element(
                By.XPATH, '//*[@id="module_product_title_1"]/div/div/span'
            ).text
            specs["name"] = name
            specs["id"] = fn[i].replace(".csv", "")
            specs["url"] = links[i]
            known_brands = [
                "dell",
                "asus",
                "acer",
                "lenovo",
                "hp",
                "msi",
                "apple",
                "huawei",
                "toshiba",
                "microsoft",
                "mi",
                "toshiba",
                "chiwi",
                "chuwi",
                "avita",
                "xlab",
                "honor",
                "dynabook",
                "razer",
                "gateway",
                "nova",
                "level51",
                "gigabyte",
            ]
            name = name.replace("-", " ")
            split_name = name.split(" ")
            b = split_name[0].lower()
            model = split_name[1] + " " + split_name[2]
            if not (b in known_brands):
                for i in range(len(split_name)):
                    string = split_name[i].lower()
                    if string in known_brands:
                        b = string
                        model = split_name[i + 1] + " " + split_name[i + 2]
                    else:
                        if string == "aspire" or string == "predator":
                            b = "acer"
                        elif string == "macbook":
                            b = "apple"
                        elif string == "expertbook":
                            b = "asus"
                        elif string == "nova":
                            b = "ripple"
                        elif (
                            string == "modern"
                            or string == "summit"
                            or string == "creator"
                            or string == "delta"
                            or re.match(r"^g\w{3}$", string)
                        ):
                            b = "msi"
                        elif (
                            string == "original"
                            or string == "pavilion"
                            or string == "vostro"
                        ):
                            b = "dell"
                        elif string == "vaio":
                            b = "sony"
                        if string == "original":
                            model = "inspiron 13"
                        else:
                            model = string + " " + split_name[i + 1]
            specs["brand"] = b
            specs["model"] = model
            pp = pd.read_csv("data/prices/" + fn[i])
            specs["price"] = int(pp.iloc[-1, -1])
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
            reviews = reviews.replace(" ratings", "")
        except:
            rating = "0"
            reviews = "0"
        specs["rating"] = rating
        specs["reviews"] = reviews

        try:
            view = driver.find_element(
                By.XPATH, '//*[@id="module_product_detail"]/div/div[2]/button'
            )
            driver.execute_script("arguments[0].scrollIntoView();", view)
            driver.execute_script("window.scrollBy(0, -100)")
            view.click()
            specheading = driver.find_element(
                By.XPATH, '//*[@id="module_product_detail"]/div/div[1]/div[3]/h2'
            )
            driver.execute_script("arguments[0].scrollIntoView();", specs)
            driver.execute_script("window.scrollBy(0, -100)")
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="module_product_detail"]/div/div/div[3]/div[1]/ul',
                    )
                )
            )
            stitle = driver.find_elements(By.CLASS_NAME, "key-title")
            svalue = driver.find_elements(By.CLASS_NAME, "key-value")
        except:
            try:
                specheading = driver.find_element(
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
                stitle = driver.find_elements(By.CLASS_NAME, "key-title")
                svalue = driver.find_elements(By.CLASS_NAME, "key-value")
            except:
                specheading = driver.find_element(
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
                stitle = driver.find_elements(By.CLASS_NAME, "key-title")
                svalue = driver.find_elements(By.CLASS_NAME, "key-value")

        titles = [stitle[i].text for i in range(2, len(stitle) - 1)]
        values = [svalue[i].text for i in range(2, len(stitle) - 1)]
        temp = pd.DataFrame(list(zip(titles, values)), columns=["Title", "Value"])
        temp.loc[:, "Title"] = temp["Title"].str.replace("_", " ")
        temp.loc[:, "Title"] = temp["Title"].apply(lambda x: x.lower())
        unwanted_data = [
            "camera front (megapixels)",
            "cpu speed (ghz)",
            "wireless connectivity",
            "input output ports",
            "battery life",
            "ac adapter",
            "model no.",
            "model",
            "generation",
            "condition",
            "storage type",
            "processor type",
            "touch pad",
            "operating system",
        ]
        temp = temp[~temp["Title"].isin(unwanted_data)]
        temp.loc[:, "Title"] = temp["Title"].str.replace(
            "storage capacity new", "storage capacity"
        )
        temp.loc[:, "Title"] = temp["Title"].str.replace(
            "number of cpu cores", "cpu cores"
        )
        temp.loc[:, "Value"] = temp["Value"].str.replace("GB", "")
        temp.loc[:, "Value"] = temp["Value"].str.replace(" Inch", "")
        temp.apply(update_specs, axis=1)
        print(i, "data/prices/" + fn[i], specs["id"], specs["brand"], specs["model"])
        dd = pd.DataFrame([specs])
        dd.to_csv(filepath, mode="a", header=not os.path.exists(filepath), index=False)

driver.delete_all_cookies()
driver.quit()
