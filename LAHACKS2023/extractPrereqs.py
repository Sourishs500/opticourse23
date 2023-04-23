

fat = 3

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

def extractPrereqs(s, dept):
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
                refinedList[i] = refinedList[i].replace("course", dept)
            else:
                refinedList[i] = refinedList[i].replace("courses", dept)

    print(refinedList)
    print(numberPrereqs)

    return refinedList

def getTotalIndex(topClass):

    classSplit = topClass.split(" ")

    dept = ""
    for item in classSplit:
        if(True in [m.isnumber() for m in item]):
            break
        else:
            dept += item


    currentPrereqs = extractPrereqs(s, dept)
    topClassPrereqsNumber = len(currentPrereqs)

    if(numberPrereqs == 0):
        return numberPrereqs

    maxNumber = 0
    nextCourse = ""

    for item in currentPrereqs:
        if(len(extractPrereqs(description, currentdepartment)) > maxNumber):
            maxNumber = len(extractPrereqs(description, currentdepartment))
            nextCourse = item

    return getTotalIndex(nextCourse) + topClassPrereqsNumber

