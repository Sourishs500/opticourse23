# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 22:41:53 2023

@author: bhata
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

url = "https://newstudents.ucla.edu/studyarea/?type=MAJ&code=402"

driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
time.sleep(1)

sections = driver.find_elements(By.TAG_NAME, "a")
for i in sections:
    

driver.quit()