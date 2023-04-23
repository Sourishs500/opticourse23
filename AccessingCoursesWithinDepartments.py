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

#establishes the driver

allLinks = pd.read_csv("DepartmentsAndLinks.csv").set_index("Department")
department = "Asian American Studies"#"Electrical and Computer Engineering"
#print(allLinks.loc["Electrical and Computer Engineering"]["Link to Courses"])
sampleDepartment = allLinks.loc[department]["Link to Courses"]

driver = webdriver.Chrome('chromedriver.exe') 
driver.get(sampleDepartment)
time.sleep(4)

courseClasses = driver.find_elements(By.XPATH, 
                                     '//div[@class="course-record"]')

print(len(courseClasses))
courseClasses = [i.get_attribute("innerHTML") for i in courseClasses]
for i in courseClasses[:5]:
    print(i)

driver.quit()

pd.Series(courseClasses).to_csv(department+"_raw_HTML_of_courses.csv")