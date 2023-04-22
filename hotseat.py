from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

fallCount = 0
winterCount = 0
springCount = 0

fallGood = False
winterGood = False
springGood = False

minimumAvailability = 70
WAIT_TIME = 10

driver = webdriver.Chrome()
driver.get("https://hotseat.io/")

className = "COM SCI 31"

#Entering class name into the hotseat search bar, waiting for items in drop down menu to appear
inputElement = driver.find_element(By.ID, "search-downshift-input-input")
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

# Now on the class page, wait for the page to load
try:
    inputElement = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, "instructor-nav"))) 
except:
    print("Sorry, your wifi is too slow :(")

inputElement = driver.find_element(By.XPATH, "/html/body/main/div/div[4]/div[2]/section[1]/div/div[2]/dd")
spanList = driver.find_elements(By.XPATH , "//*[contains(@class, 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100')]")
# find TERMS OFFERED

# range needs to be adjusted based on how many terms are listed
for i in range(len(spanList) + 1):
    inputElement = driver.find_element(By.XPATH, '/html/body/main/div/div[4]/div[2]/section[1]/div/div[2]/dd/span[' + str(i+1)+']')
    termOffered = inputElement.text[2]
    yearOffered = inputElement.text[0:2]


    if(i == 0):
        mostRecentYear = int(yearOffered)
    if(i == 18):
        leastRecentYear = int(yearOffered)
    if(termOffered == "F"):
        fallCount = fallCount + 1
    elif(termOffered == "S"):
        springCount = springCount + 1
    else:
        winterCount = winterCount + 1

fallPercentage = (fallCount / (mostRecentYear - leastRecentYear + 1)) * 100
winterPercentage = (winterCount / (mostRecentYear - leastRecentYear + 1)) * 100
springPercentage = (springCount / (mostRecentYear - leastRecentYear + 1)) * 100


if(fallPercentage > minimumAvailability):
    fallGood = True
if(winterPercentage > minimumAvailability):
    winterGood = True
if(springPercentage > minimumAvailability):
    springGood = True

if(fallGood):
    print(className + " is good for fall" + "\n")
if(winterGood):
    print(className + " is good for winter" + "\n")
if(springGood):
    print(className + " is good for spring" + "\n")

driver.quit()



