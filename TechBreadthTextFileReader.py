# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 05:25:28 2023

@author: bhata
"""

def getTechBreadthCourses(choice):
    A = {}
    with open("Technical Breadth Recommendations.txt") as file:
        for line in file:
            myLine = line.split(": ")
            myLine[1] = myLine[1].split(", ")
            A[myLine[0]] = myLine[1]
    return A[choice]

'''
Computer Science: MATH 61, COM SCI 180, COM SCI M152A
Computational Genomics: LIFESCI 7A, LIFESCI 7B, LIFESCI 7C
Engineering Mathematics: MATH 61, MATH 115A, MATH 131A
Technology Management: ENGR 110, ENGR 111, ENGR 112
'''

print(getTechBreadthCourses("Computer Science"))
print(getTechBreadthCourses("Computational Genomics"))
print(getTechBreadthCourses("Engineering Mathematics"))
print(getTechBreadthCourses("Technology Management"))
