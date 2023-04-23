# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 01:41:22 2023

@author: bhata
"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
from word2number.w2n import word_to_num


major = "Electrical Engineering B.S." #input

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
    
    #print(len(courseClasses))
    courseClasses = [i.get_attribute("innerHTML") for i in courseClasses]
    #for i in courseClasses[:5]:
    #    print(i)
    
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

    for i in range(len(reqs)):
        if (len(coreqs[i]) != 0):
            reqs[i] = reqs[i] + ", "
        requisites.append(reqs[i] + coreqs[i])
    
    for i in range(len(requisites)):
        if len(requisites[i])>1:
            requisites [i] = [k.replace(",", "") for k in requisites[i].split()]
            #for j in len(requisites[i]):
            
                
            if (requisites[i][0]=="course"):
                if True in [m.isnumeric() for m in requisites[i][1]]:
                    requisites[i][0] = dept
            elif requisites[i][0]=="courses":
                if True in [m.isnumeric() for m in requisites[i][1]]:
                    requisites[i][0] = dept
                if len(requisites[i])>=4:
                    requisites[i][3] = dept+" "+requisites[i][3]
            requisites[i] = " ".join(requisites[i])
    
    
    
    finaldf = pd.DataFrame(list(zip(courselist, unitcounts, requisites, li)), columns=['Course Title', 'Unit Count', 'Requisites', 'Course Description'])
    finaldf["Requisites"] = finaldf["Requisites"].apply(lambda x: x.strip().rstrip())
    
    finaldf.to_csv(dept + ".csv")
    return finaldf



baseURL = "https://catalog.registrar.ucla.edu/major/2022/"
fullURL = baseURL + "".join([i for i in major if i.isalnum()])
driver = webdriver.Chrome('chromedriver.exe') 
driver.get(fullURL)
time.sleep(0.5)


majorInfo = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'main-content')]")
#print(majorInfo[0].get_attribute("class"), "\n\n\n")

majorInfo = majorInfo[0].find_elements(By.XPATH, "./child::*")
majorInfo = ([BeautifulSoup(i.get_attribute("innerHTML"), "html.parser") for i in majorInfo])#get_attribute("name")

ACTUAL = majorInfo[3]


driver.quit()

A = BeautifulSoup(ACTUAL.prettify().replace("span", "br").replace("keyboard_arrow_down", "").replace("Expand all", ""), 
                  "html.parser").text
for i in range(3):
    A = A.replace("\n\n", "\n")#.replace("\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n")

file = A.split("\n")

# File to list of lines
lines = []
lines_extras = []
extrasDetect = False
for line in file:
    # After first instance of extras like honors in text, rest of text goes to extras list instead of normal list
    if extrasDetect == False and ('Honors' in line):
        extrasDetect = True
    # Include line if not empty and contains keywords
    if (line.rstrip() != '') and ('Complete' in line or 'course' in line or ('Select' in line and 'from' in line) or line.lstrip()[1].isupper() or line.lstrip()[1] == '&' or line.lstrip()[1] == ' '):
        if not extrasDetect:
            lines.append(line.rstrip().split(' - ', 1)[0]) # split: remove text after course number
        else:
            lines_extras.append(line.rstrip().split(' - ', 1)[0]) # split: remove text after course number

# Find first instance of a number in a list and return it
def find_first_num(list):
    for word in list:
        try:
            return word_to_num(word)
        except ValueError:
            continue
    return 1

courses = [] # All courses
selection = [] # Courses when there is an option to pick between multiple course
complete_counter = 0 # Counter for adding courses when 'Complete x courses' is detected
select = False # Boolean for optional mode (adding courses to selection) vs. normal mode (adding courses directly to courses)
select_counter = 1
for line in lines:
    # curr_leading_spaces = len(line) - len(line.lstrip())
    
    if 'Complete' in line:
        if (select and len(selection) != 0):
            for i in range(select_counter):
                courses.append(selection.copy())
                if complete_counter > 0:
                    complete_counter -= 1
        select = False
        selection.clear()
        
        words = line.split()
        if complete_counter == 0:
            complete_counter = find_first_num(words)
    elif 'Select' in line:
        if (select and len(selection) != 0):
            for i in range(select_counter):
                courses.append(selection.copy())
                if complete_counter > 0:
                    complete_counter -= 1
        select = False
        selection.clear()

        words = line.split()
        select = True
        select_counter = find_first_num(words)
    elif select and (line.lstrip()[1].isupper() or line.lstrip()[1] == '&' or line.lstrip()[1] == ' '): # If select mode is on and line has a course number
        selection.append(line.lstrip())
    elif complete_counter > 0 and (line.lstrip()[1].isupper() or line.lstrip()[1] == '&' or line.lstrip()[1] == ' '):
        courses.append(line.lstrip())
        complete_counter -= 1

    # print(line)
    # print(f'complete: {complete_counter} select: {select} select_counter: {select_counter}')
    # print(courses)
    # print(selection)

if (len(selection) != 0):
    for i in range(select_counter):
        courses.append(selection.copy())

findPrereqsFor = []    
    
#for course in courses:
#    if sum([i.isnumeric() for i in course])>3:
        
import random    
finalDegreePlan = []
for i in courses:
    if (type(i)==str):
        finalDegreePlan.append(i)
    else:
        randomChoice = random.randint(0, len(i)-1)
        while (i[randomChoice] in finalDegreePlan):
            randomChoice = random.randint(0, len(i)-1)
        finalDegreePlan.append(i[randomChoice])

courses = finalDegreePlan

for course in courses:
    print(course)


setOfDepartments = []
for i in courses:
    if (type(i)==str):
        setOfDepartments.append(" ".join(i.split()[:-1])  )
        #print(i)

setOfDepartments = list(set(setOfDepartments))


importedDepartments = pd.read_csv("DepartmentAbbKey.csv")
print(importedDepartments)

importedDepartments = importedDepartments.set_index("Abbreviation")["Department"]
specificImportedDepartments = list(importedDepartments.loc[setOfDepartments].values)

departmentPlusCoursesPlusPrereqs = {}
for i in specificImportedDepartments:
    depToCSV(i)
    print(i)