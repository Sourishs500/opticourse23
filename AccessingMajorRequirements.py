# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 08:16:03 2023

@author: bhata
"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests


major = "Computer Science and Engineering B.S."#"Electrical Engineering B.S." #input



baseURL = "https://catalog.registrar.ucla.edu/major/2022/"
fullURL = baseURL + "".join([i for i in major if i.isalnum()])
driver = webdriver.Chrome('chromedriver.exe') 
driver.get(fullURL)
time.sleep(0.5)


majorInfo = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'main-content')]")
print(majorInfo[0].get_attribute("class"), "\n\n\n")

majorInfo = majorInfo[0].find_elements(By.XPATH, "./child::*")
majorInfo = ([BeautifulSoup(i.get_attribute("innerHTML"), "html.parser") for i in majorInfo])#get_attribute("name")

ACTUAL = majorInfo[3]


driver.quit()

A = BeautifulSoup(ACTUAL.prettify().replace("span", "br").replace("keyboard_arrow_down", "").replace("Expand all", ""), 
                  "html.parser").text
for i in range(3):
    A = A.replace("\n\n", "\n")#.replace("\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n")

textFile = open(major+"_DegreeRequirements.txt", "w")
textFile.write(A)
textFile.close()