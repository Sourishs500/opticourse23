import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
from word2number.w2n import word_to_num


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

for course in courses:
    print(course)