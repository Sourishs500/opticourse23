# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome('chromedriver.exe') 
#establishes the driver

print("Driver established")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
driver.get('https://registrar.ucla.edu/academics/course-descriptions') 
#gets the page
time.sleep(1)
courses = driver.find_elements(By.XPATH, '/html/body/main/div/div/div[2]/div/div/div/div/div/div'+"/div/ol/li/a")
print(len(courses), "departments found")
depts = {}
for i in courses:
    depts[i.text] = i.get_attribute("href")

for i in depts.keys():
    print(i, ":", depts[i], "\n")
driver.quit()

import pandas as pd

pd.Series(depts).reset_index().rename(columns = {"index":"Department", 0:"Link to Courses"}).set_index("Department").to_csv("DepartmentsAndLinks.csv")