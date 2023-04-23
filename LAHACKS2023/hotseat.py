from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests as r

def hotseat(className):
    fallCount = 0
    winterCount = 0
    springCount = 0
    summerCount = 0
    firstPass = False
    demandIndex = 70

    altFour = "2023-02-22T23"
    altThree = "2023-02-22T22"
    firstPassDate = "2023-02-22T21"
    altFirstPassDate = "2023-02-22T20"
    altTwo = "2023-02-22T19"


    fallGood = False
    winterGood = False
    springGood = False

    allTerms = []

    minimumAvailability = 70
    WAIT_TIME = 10
    CURRENT_YEAR = 23

    mostRecentYear = 23
    leastRecentYear = 23

    driver = webdriver.Chrome()
    driver.get("https://hotseat.io/")

    # THE ONLY VARIABLE THAT NEEDS TO CHANGE
    # className = "COM SCI 31"

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
    if(className == "MATH 33A" or className == "MATH 33B"):
        inputElement = driver.find_element(By.ID, "search-downshift-input-item-1")
    else:
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

        if(inputElement.text in allTerms):
                continue
        else:
            allTerms.append(inputElement.text)

        if(int(yearOffered) <= CURRENT_YEAR - 9):
            leastRecentYear = int(yearOffered)
            break


        if(i == 0):
            mostRecentYear = int(yearOffered)
        if(i == len(spanList)):
            leastRecentYear = int(yearOffered)
        if(termOffered == "F"):
            fallCount = fallCount + 1
        elif(termOffered == "S"):
            springCount = springCount + 1
        else:
            winterCount = winterCount + 1

    # Finding first pass enrollment information
    inputElement = driver.find_element(By.XPATH, "/html/body/main/div/div[4]/div[1]/div[1]")
    enrollmentCard = inputElement.get_attribute("data-react-props")

    firstPassinfo = ""
    secondPassTime = "never gonna be mentioned"

    splitUpEnrollmentCard = enrollmentCard.split("{")

    #gotta remove secondPassTime from the list

    for i in splitUpEnrollmentCard:
        if(i.find("Second") > 0):
            secondPassTime = i[i.find("time") + 7 : i.find("time") + 20]
            year = int(secondPassTime[:4])
            month = int(secondPassTime[5:7])
            day = int(secondPassTime[8:10])
            hour = int(secondPassTime[11:13]) - 15
            continue
        
        #if(i.find(firstPassDate) > 0 or i.find(altFirstPassDate) > 0 or i.find(altTwo) > 0 or i.find(altThree) > 0 or i.find(altFour) > 0):
            #firstPassinfo = i
        # break
        start = i.find("createdAt")
        if(start > 0):
            currentYear = int(i[start + 12 : start + 16])
            currentMonth = (i[start + 17 : start + 19])
            currentDay = (i[start + 20 : start + 22])
            currentHour = (i[start + 23 : start + 25])
            
            if((int(currentYear) == year and int(currentMonth) >= month and int(currentDay) >= day and int(currentHour) >= hour)):
                firstPassinfo = i
                break



    firstPassinfo = firstPassinfo[firstPassinfo.find("enrollmentCount"):]


    firstPassenrollmentCount = float(firstPassinfo[firstPassinfo.find(":") + 1 :firstPassinfo.find(",")])
    firstPassinfo = firstPassinfo[firstPassinfo.find(",") + 1:]
    enrollmentCapacity = float(firstPassinfo[firstPassinfo.find(":") + 1 :firstPassinfo.find(",")])

    enrollPercentageByFirstPass = (firstPassenrollmentCount / enrollmentCapacity) * 100
    print(enrollPercentageByFirstPass)





    if(enrollPercentageByFirstPass > demandIndex):
        firstPass = True

    # Traversing through all professors for the class

    courseInstructorList = driver.find_elements(By.XPATH, "//*[contains(@class, 'course-instructor-tab')]" )
    initialInstructorAmount = len(courseInstructorList)

    page_source = driver.page_source
    #get_url = driver.current_url

    for i in range(2, initialInstructorAmount):
        inputElement = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div/nav/a[" + str(i) + "]")
        mostRecentYearTaught = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div/nav/a[" + str(i) + "]/span").text[0:2]
        if(int(mostRecentYearTaught) <= CURRENT_YEAR - 9):
            continue
        
        instructorLink = inputElement.get_attribute('href')
        driver.get(instructorLink)

        try:
            inputElement = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, "instructor-nav"))) 
        except:
            print("Sorry, your wifi is too slow :(")
        
        inputElement = driver.find_element(By.XPATH, "/html/body/main/div/div[4]/div[2]/section[1]/div/div[2]/dd")
        spanList = driver.find_elements(By.XPATH , "//*[contains(@class, 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100')]")
        # find TERMS OFFERED

        # range needs to be adjusted based on how many terms are listed
        for i in range(1, len(spanList)):
            inputElement = driver.find_element(By.XPATH, '/html/body/main/div/div[4]/div[2]/section[1]/div/div[2]/dd/span[' + str(i)+']')
            # print(inputElement.text + "\n")
            termOffered = inputElement.text[2:]
            yearOffered = inputElement.text[0:2]

            if(inputElement.text in allTerms):
                continue
            else:
                allTerms.append(inputElement.text)

            if(int(yearOffered) <= CURRENT_YEAR - 9):
                leastRecentYear = int(yearOffered)
                break

            if(i == len(spanList) - 1):
                if(int(yearOffered) < leastRecentYear):
                    leastRecentYear = int(yearOffered)
            if(termOffered == "F"):
                fallCount = fallCount + 1
            elif(termOffered == "S"):
                springCount = springCount + 1
            elif(termOffered == "W"):
                winterCount = winterCount + 1
            else:
                summerCount = summerCount + 1


    #soup = BeautifulSoup(page_source, "html.parser")
    # a_href=soup.find_all("a",{"class":"course-instructor-tab"}).get("href")

    fallPercentage = (fallCount / (mostRecentYear - leastRecentYear + 1)) * 100
    winterPercentage = (winterCount / (mostRecentYear - leastRecentYear + 1)) * 100
    springPercentage = (springCount / (mostRecentYear - leastRecentYear + 1)) * 100
    summerPercentage = (summerCount / (mostRecentYear - leastRecentYear + 1)) * 100

    if(fallPercentage > minimumAvailability):
        fallGood = True
    if(winterPercentage > minimumAvailability):
        winterGood = True
    if(springPercentage > minimumAvailability):
        springGood = True

    """
    if(fallGood):
        print(className + " is good for fall: offered " + str(int(fallPercentage)) + "% of the time in the fall" + "\n")
    if(winterGood):
        print(className + " is good for winter: offered " + str(int(winterPercentage)) + "% of the time in the winter" +  "\n")
    if(springGood):
        print(className + " is good for spring: offered " + str(int(springPercentage)) + "% of the time in the spring" + "\n")
    if(firstPass):
        print(className + " should be first passed!")
    else:
        print(className + " should be second passed!")

    print(allTerms)
    """


    driver.quit()

    return [fallGood, winterGood, springGood, fallPercentage, winterPercentage, springPercentage]



