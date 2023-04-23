# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:57:20 2023

@author: bhata
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests

url = "https://admission.ucla.edu/apply/majors"

driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
time.sleep(1)

sections = driver.find_elements(By.TAG_NAME, "a")

allMajors = {}
majorList = []

for i in sections:
    A = i.get_attribute("href")
    if ("studyarea" in A):
        allMajors[i.text] = A
        majorList.append(i.text)


allMajors = pd.Series(allMajors).reset_index().rename(columns = {"index":"Major", 0:"Link"}).set_index("Major")#.to_csv("LinkForMajorReqsPerMajor.csv")
pd.Series(majorList).reset_index()[[0]].rename(columns = {0:"Major"}).to_csv("List of Majors.csv")
























'''
allMajors["Preparation for the Major"] = ""
allMajors["The Major"] = ""


for i in allMajors.index:#[i for i in allMajors.index if "Electrical" in i]:
    link = allMajors.loc[i].loc["Link"]
    
    driver2 = webdriver.Chrome('chromedriver.exe')
    driver2.get(link)
    time.sleep(1)
    
    links = driver2.find_elements(By.TAG_NAME, "a")
    links = [i.get_attribute("href") for i in links]
    links = [i for i in links if i!=None]
    links = [i for i in links if "registrar" in i][0]
    print(links)
    
    driver2.get(links)
    time.sleep(1)
    
    divs = driver2.find_elements(By.TAG_NAME, "div")

    prep = [i for i in divs if "PreparationfortheMajor" in i.get_attribute("id")]
    if len(prep) > 0:
        prep = prep[0]
        prep = BeautifulSoup(prep.find_element(By.XPATH, "../div[2]").get_attribute("innerHTML"), "html.parser").text
    else:
        prep = "No preparation courses found on website"
    
    theMaj = [i for i in divs if "TheMajor-" in i.get_attribute("id")]
    if len(theMaj) > 0:
        theMaj = theMaj[0]
        theMaj = BeautifulSoup(theMaj.find_element(By.XPATH, "../div[2]").get_attribute("innerHTML"), "html.parser").text
    else:
        theMaj = "No major courses found on website"
    
    allMajors.loc[i, "Preparation for the Major"] = prep
    allMajors.loc[i, "The Major"] = theMaj

    driver2.quit()
    
allMajors.to_csv("Major Components.csv")'''
driver.quit()