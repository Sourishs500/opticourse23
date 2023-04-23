# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 14:33:13 2023

@author: bhata
"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests

import requests

allLinks = pd.read_csv("DepartmentsAndLinks.csv").set_index("Department")
driver = webdriver.Chrome('chromedriver.exe')
B = {}
index = 1
i=0
while (i<(len(allLinks))):
    driver.get(allLinks.iloc[i].iloc[0])
    time.sleep(0.25)
    A = driver.find_elements(By.TAG_NAME, "div")
    #print([i.text for i in A])
    A = [i.text for i in A if "block-ucla" in i.get_attribute("id")]
    print(index, ". Title:", A)
    A = A[0]
    if (" (" in A):
        A = [i[:-1] for i in A.split("(")]
        B[A[0]] = A[1]
        index+=1
        i+=1

driver.quit()