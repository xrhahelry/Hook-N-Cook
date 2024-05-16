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
df = pd.read_csv("data/urls_2.csv")
links = df["Url"]
fn = df["Filename"]
filepath = "data/smartphones.csv"