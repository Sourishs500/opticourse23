# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 14:16:16 2023

@author: bhata
"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests

school = "Letters and Sciences"#"Engineering"
spreadsheet = "LA Hacks Opti-Course GE Map.xlsx"


Writing1Prompt = "Do you have Writing I satisfied? (you probably do if you have credit for some college-level English course)"
EthicsPlusEngWritingPrompt = "Would you like to satisfy the Ethics and Engineering Writing requirements with a single course?"
SIPreferencePrompt = "Would you be willing to work harder for a physical science class or a life science class (you must pick one)?"
SIPreferenceForLabPrompt = "Would you prefer to fulfill the 'lab' category when you do this harder class or would you prefer to knock out your Writing II requirement with this harder science class?"
FLLevelPrompt = "What level of any foreign language do you think you can test into (1, 2, 3, 4, or 5)?"
QuantPrompt = "Have you satisfied the Quantitative Reasoning requirement? (you probably have if you have taken college-level math courses before)"


AH = True
SC = True
SI = True

FL = (school in ["Letters and Sciences", "Arts and Architecture", "Music"])
WritingII = (school!="Engineering")
Diversity = not(school in ["Engineering", "Nursing"])
EngWriting = (school=="Engineering")
TechBreadth = (school=="Engineering")
Ethics = (school=="Engineering")
Quantitative = (school == "Arts and Architecture")


df = (pd.read_excel(spreadsheet).applymap(lambda x: str(x).replace("\n", " ")).T
                                .iloc[:7].T.rename(columns = {"Unnamed: 0":"School"})
                                .iloc[1:].set_index("School"))

numberOfGEs = sum([sum(eval(i)[0]) for i in df.loc[school].iloc[:3].values])


#Determined by user input
WritingIIDesiredArea = "LCA"
DiversityDesiredArea = "SA"
WritingI = False
if FL:
    FL = True
if Quantitative:
    Quantitative = True
preferenceDictionary = (
    {
     'Arts/Humanities':{
           "LCA":1,
           "VPAA":2,
           "PLA":3,
          },
     'Society/Culture':{
           "SA":2,
           "HA":1,
          },
     'Scientific Inquiry':{
           "PS":1,
           "LS":2,
          }
    }
)
#Determined by user input

mainGEs = df.loc[school].iloc[:3]

orderDictionary = {    
    'Arts/Humanities':["LCA", "PLA", "VPAA"],
    'Society/Culture':["HA", "SA"],
    'Scientific Inquiry':["LS", "PS"]
    }

ultimateGEDict = {}

for area in orderDictionary.keys():
    courseReqsForArea = list(eval(df.loc[school].loc[area])[0])
    print(courseReqsForArea)
    for i in range(len(orderDictionary[area])):
        
        currentCourseAsSetByMe = orderDictionary[area][i]
        print(currentCourseAsSetByMe)
        
        rankingOfCurrentCourse = preferenceDictionary[area][currentCourseAsSetByMe]+len(orderDictionary[area])-1
        courseReqsForArea[i] += courseReqsForArea[rankingOfCurrentCourse]
    courseReqsForArea = courseReqsForArea[:len(orderDictionary[area])]
    print(courseReqsForArea)
    
    ultimateGEDict[area] = pd.DataFrame(index = orderDictionary[area], 
                                        columns = ["Course Count", "Writing II", 
                                                   "Diversity"])
    ultimateGEDict[area]["Course Count"] = courseReqsForArea
    if WritingIIDesiredArea in orderDictionary[area] and WritingII:
        ultimateGEDict[area].at[WritingIIDesiredArea, "Writing II"] = 1
    if DiversityDesiredArea in orderDictionary[area] and Diversity:
        ultimateGEDict[area].at[DiversityDesiredArea, "Diversity"] = 1

for i in ultimateGEDict.keys():
    print(ultimateGEDict[i])




theTrueGOATlink = "https://sa.ucla.edu/ro/Public/SOC/Search/SearchByFoundation?input=%7B%22FoundationCode%22%3A%22AH%22%2C%22CategoryCode%22%3A%22LC%22%2C%22LabDemoFilter%22%3Afalse%2C%22WritingTwoFilter%22%3Afalse%2C%22MultiCategoryFilter%22%3Afalse%2C%22DiversityFilter%22%3Afalse%7D&search_criteria=Foundations+of+Arts+and+Humanities&_=1682231470892"
page = requests.get(theTrueGOATlink)
soupy = BeautifulSoup(page.text, "html.parser")
print(soupy.prettify())








'''
driver = webdriver.Chrome('chromedriver.exe')

i = 0
currentBroadCategory = list(ultimateGEDict.keys())[i]
print(currentBroadCategory)

j = 0
currentNarrowCategory = ultimateGEDict[currentBroadCategory].index[j]

driver.get("https://sa.ucla.edu/ro/Public/SOC/Search/GECoursesMasterList")
time.sleep(1)

shadow_section = driver.execute_script(
    "return document.querySelector('ucla-sa-soc-app').shadowRoot"
)

element = shadow_section.find_elements(By.ID, "webComponentWrapper")[0].find_elements(By.ID, "layoutContentArea")
element = element[0].find_element(By.ID, "soc-search").find_element(By.ID, "partial-search")
element = element.find_element(By.ID, "div_simple_search").find_element(By.ID, "search_panel")
element = element.find_element(By.ID, "partial_content").find_element(By.ID, "div_geclass")
element = element.find_element(By.ID, "div_foundationclasses").find_element(By.ID, "select_soc_filter_geclasses_foundation")
#element = element.find_element(By.XPATH, "//")#.shadowRoot
element2 = driver.execute_script('''#return document.querySelectorAll("input")''')

#print(element2.get_attribute("id"))
#element2 = element[0].shadowRoot
#shadow_root = driver.execute_script('return document.querySelector("ucla-sa-soc-app").shadowRoot')
#element = shadow_root.execute_script('return document.querySelector("input")')
# inputBox = shadow_section.find_elements(By.TAG_NAME, "input")
#print(inputBox.get_attribute("type"))


'''
from selenium import webdriver

# create a new Chrome driver
driver = webdriver.Chrome()

# navigate to the webpage with the shadow-root element
driver.get("https://example.com%22/)

# find the shadow-root element using JavaScript
shadow_root = driver.execute_script('return document.querySelector("your-shadow-root-selector").shadowRoot')

# find the element inside the shadow-root using JavaScript
element = shadow_root.execute_script('return document.querySelector("your-inner-element-selector")')

# interact with the element as needed
element.click()

# close the driver
driver.quit()
'''



























#inputBoxes = driver.find_element(By.ID, "shadow_host")
#script = 'return arguments[0].shadowRoot'
#shadow_root = driver.execute_script(script, shadow_host)
#shadow_section = driver.execute_script(
#    '''return document.querySelector("neon-animatable").shadowRoot''')
#inputBox = driver.find_element(By.ID, "webComponentWrapper")
#print(inputBox.get_attribute("id"))




#print([i.get_attribute("title") for i in inputBoxes])
#print(inputBoxes.get_attribute("title"))# if i.get_attribute("id")=="search_panel"])



#driver.quit()
'''
driver = webdriver.Chrome()
driver.get("https://hotseat.io/%22)

className = "COM SCI 32"

#Entering class name into the hotseat search bar, waiting for items in drop down menu to appear
inputElement = driver.find_element(By.ID, "search-downshift-input-input")
# Entering the class name into text box
inputElement.send_keys(className)

# Wait until the first item (the class we want) appears
try:

    inputElement = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, "search-downshift-input-item-0"))) 
except:
    print("Sorry, your wifi is too slow :(")

# Hover over the element (may or may not be needed)
inputElement = driver.find_element(By.ID, "search-downshift-input-item-0")
hover = ActionChains(driver).move_to_element(inputElement)
hover.perform()

inputElement.click()
'''