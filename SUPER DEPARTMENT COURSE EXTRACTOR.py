# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 01:31:05 2023

@author: bhata
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup



department = "Electrical and Computer Engineering"

def depToCSV(department):
    #establishes the driver
    allLinks = pd.read_csv("DepartmentsAndLinks.csv").set_index("Department")
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
    
    dept = department
    df = pd.Series(courseClasses).reset_index().rename(columns = {"index":"", 0:"0"})
    raw = df['0'].values.tolist()
    
    # format list elements - raw contains mostly formatted course elements
    raw=[ i.replace("<h3>", "") for i in raw]
    raw=[ i.replace("</h3>", "\n") for i in raw]
    raw=[ i.replace("<p>", "") for i in raw]
    raw=[ i.replace("</p>", "\n") for i in raw]
    li=[ i + "\n" for i in raw]
    
    courselist=[ i[:i.find("\n")] for i in li ]
    
    # omit course name
    raw=[ i.replace(i, i[1 + i.find("\n"):]) for i in li]
    
    unitcounts=[ i[7:i.find("\n")] for i in raw ]
    
    # omit unit count
    raw=[ i.replace(i, i[1 + i.find("\n"):]) for i in raw]
    
    # raw contains description only
    
    # final requisites list
    requisites = []
    
    # temp reqs
    reqs = []
    
    # temp coreqs
    coreqs = []
    
    s = ""
    for i in range(len(raw)):
        s = raw[i]
        ind = s.find("equisite")
        if (ind == -1):
            reqs.append("")
            coreqs.append("")
        else:
            ind = s.find(":")
            if (ind != -1):
                s = s[ind + 2:]
                reqs.append(s[:s.find(".")])
            else:
                reqs.append("")
    
            s = s[s.find(".") + 2:]
            ind = s.find("equisite")
    
            if (ind == -1):
                coreqs.append("")
            else:
                ind = s.find(":")
                if (ind == -1):
                    coreqs.append("")
                else:
                    s = s[ind + 2:]
                    coreqs.append(s[:s.find(".")])
    
    for i in range(len(reqs)):
        if (len(coreqs[i]) != 0):
            reqs[i] = reqs[i] + ", "
        requisites.append(reqs[i] + coreqs[i])
    
    finaldf = pd.DataFrame(list(zip(courselist, unitcounts, requisites, li)), columns=['Course Title', 'Unit Count', 'Requisites', 'Course Description'])
    finaldf["Requisites"] = finaldf["Requisites"].apply(lambda x: x.strip().rstrip())
    
    finaldf.to_csv(dept + ".csv")