import pandas as pd
import GetALLCoursesAndPrereqsForAMajor___BIG as creator

def __init__():
    return 

def makeATable(table_data):
    # Create the HTML table
    html_table = '<table>\n'

    # Add the table header
    html_table += '<tr>\n'
    for header in table_data[0]:
        html_table += f'<th>{header}</th>\n'
    html_table += '</tr>\n'

    # Add the table data
    for row in table_data[1:]:
        html_table += '<tr>\n'
        for cell in row:
            html_table += f'<td>{cell}</td>\n'
        html_table += '</tr>\n'

    # Close the HTML table
    html_table += '</table>'

    # Return the HTML table
    return (html_table)




    

    

# Pulls out prereqs from the prereq column of the csv file returned by pdtoCSV()
def extractPrereqs(topClass):

    # Short form department of the course
    splitCourse = " ".join(topClass.split(" ")[:-1])
    # Course number
    courseNumber = topClass.split(" ")[-1]

    # Long form of the department of a course in the major course list
    longFormDept = creator.importedDepartments.loc[splitCourse]

    # Making dataframe with all courses of that majors' department
    prereqCSV = creator.depToCSV(longFormDept)

    # Limiting the dataframe to only the entry with this major course
    prereqCSV = prereqCSV[prereqCSV["Course Title"].str.contains(courseNumber+".")]

    # Extracting string for prereqs (raw string)
    s = prereqCSV["Requisites"].iloc[0]

    s = s.replace(")", ", course")
    s = s.replace("(", "")

    list = s.split(" ")
    refinedList = []
    numberPrereqs = 0

    keyIndex = 0
    lastNumberIndex = 0

    takeNextOne = False
    lastKeyWord = ""
    seenNumber = False

    keywords = ["Computer", "Science", "Engineering", "Environmental", "Math", "Stat", "Civil", "Mech", "Aero", "Data", "Physics", "course"]

    #if a keyword is behind a number, then that keyword should be attached to that number
    for item in list:

        if True in [m.isnumeric() for m in item]:
            refinedList.append(lastKeyWord + " " + item)
            numberPrereqs += 1
            seenNumber = True
        else:
            for word in keywords:
                if (item.find(word) >= 0):
                    if(seenNumber == True):
                        seenNumber = False
                        lastKeyWord = item
                    else:
                        lastKeyWord = lastKeyWord + " " + item


    for i in range(len(refinedList)):
        refinedList[i] = refinedList[i].strip()
        refinedList[i] = refinedList[i].replace(",", "")
        if (refinedList[i].find("course") != -1):
            if(refinedList[i].find("courses") == -1):
                refinedList[i] = refinedList[i].replace("course", splitCourse)
            else:
                refinedList[i] = refinedList[i].replace("courses", splitCourse)

    return refinedList






def getTotalIndex(topClass):

    # Extracting list of prereqs (organized)
    currentPrereqs = extractPrereqs(topClass)

    topClassPrereqsNumber = len(currentPrereqs)

    if(topClassPrereqsNumber == 0):
        return topClassPrereqsNumber

    maxNumber = 0
    nextCourse = ""

    for item in currentPrereqs:
        if(len(extractPrereqs(item)) > maxNumber):
            maxNumber = len(extractPrereqs(item))
            nextCourse = item

    topClass = nextCourse

    return getTotalIndex(topClass) + topClassPrereqsNumber






def bigFunction(major):
    creator.major = major
    # Creates a course list of all major courses
    majorCourseList = creator.courses
    prereqList = []
    allPrereqs = []
    courseIndex = 0

    courseWithPreReqs = {}

    # Iterating through every major requirement course
    for course in majorCourseList:

        # Extracting list of prereqs (organized)
        prereqList = extractPrereqs(course)

        courseIndex = getTotalIndex(course)

        # Compiling a big list of courses
        majorCourseList += prereqList

        # Adding all prereqs to a big prereqlist
        allPrereqs.append(prereqList)

        courseWithPreReqs[course] = courseIndex
    
    majorCourseList = list(set(majorCourseList))

    return courseWithPreReqs
    


