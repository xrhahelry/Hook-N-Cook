from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import re

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disk-cache-size=0")

service = Service(executable_path="data/scraper/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
df = pd.read_csv("data/urls.csv")
links = df["Url"]
fn = df["Filename"]
filepath = "data/laptops.csv"
data = pd.read_csv("data/laptops.csv")
old = data["id"].to_list()


def update_specs(row):
    title = row["Title"]
    value = row["Value"]
    if title in specs:
        specs[title] = value


for x in range(len(links)):
    if fn[x].replace(".csv", "") in old:
        pp = pd.read_csv("data/prices/" + fn[x])
        data.loc[data.id == fn[x].replace(".csv", ""), "price"] = int(pp.iloc[-1, -1])
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
            "operating system": None,
            "ram memory": None,
            "display size": None,
            "storage capacity": None,
            "cpu cores": None,
            "graphics card": None,
            "graphics memory": None,
            "touch": None,
            "rating": None,
            "reviews": None,
            "name": None,
            "url": None,
        }
        driver.get(links[x])
        print(x, links[x])
        try:
            name = driver.find_element(
                By.XPATH, '//*[@id="module_product_title_1"]/div/div/span'
            ).text
            specs["name"] = name
            specs["id"] = fn[x].replace(".csv", "")
            specs["url"] = links[x]
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
            pp = pd.read_csv("data/prices/" + fn[x])
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
        temp = temp[
            (temp["Title"] != "camera front (megapixels)")
            & (temp["Title"] != "cpu speed (ghz)")
            & (temp["Title"] != "wireless connectivity")
            & (temp["Title"] != "input output ports")
            & (temp["Title"] != "battery life")
            & (temp["Title"] != "ac adapter")
            & (temp["Title"] != "model no.")
            & (temp["Title"] != "model")
            & (temp["Title"] != "generation")
            & (temp["Title"] != "condition")
            & (temp["Title"] != "storage type")
            & (temp["Title"] != "processor type")
            & (temp["Title"] != "touch pad")
        ]
        temp.loc[:, "Title"] = temp["Title"].str.replace(
            "storage capacity new", "storage capacity"
        )
        temp.loc[:, "Title"] = temp["Title"].str.replace(
            "number of cpu cores", "cpu cores"
        )
        temp.loc[:, "Value"] = temp["Value"].str.replace("GB", "")
        temp.loc[:, "Value"] = temp["Value"].str.replace(" Inch", "")
        temp.apply(update_specs, axis=1)
        print(specs)
        dd = pd.DataFrame([specs])
        dd.to_csv(filepath, mode="a", header=not os.path.exists(filepath), index=False)

driver.delete_all_cookies()
driver.quit()
