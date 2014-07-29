#!/usr/bin/python
# Analyze Chicago's food inspection data
# and make a series of tasty pie charts and tables
# • Outcomes of a health-inspection (pass, fail)
# • Risk levels
# • Breakdown of establishment types
# • Most common code violations
import csv
import matplotlib
import re

def makeChart(subsetDict):
"""
Takes a dictionary with the subset of data that we want and makes a chart 
""" 
    label_list = [subsetDict.keys() ]  #turns keys int a a list
    wedges = [subsetDict[x] for x in subsetDict.keys()] # turns data into a list with the same order
    matplotlib.pyplot.pie (  wedges, labels=label_list)
    matplotlib.pyplot.show()
    return None
def inspectionResults(foodDict) :
"""
This makes a very basic pie chart that shows how often eateries pass inspection  
"""  
    # pull out inspection data
    iDict = {}
    return makeChart(iDict)

def commonViolationsChart(foodDict):
"""
Prints a pie chart demonstrating the most common violations of health code cited 
"""    
    # pull out violation data
    return makeChart(vDict)
def restaurantsTypes(foodDict):
"""
Prints a pie chart demonstrating the proportions of restaurant types
"""    
    # pull out restaurant type data
    return makeChart(rDict)
def relativeRisk(foodDict):
"""
makes a bar chart comparing the violation percentage by restaurant type
"""
    #for each violation keep of tally of the associated restaurant type
    #compare to the total number restaurants in that type
def typeOfLine(row):
"""
this csv has many types of rows thrown together.  This fuction returns the type of row.
"""
    keyRE = r'' # re to match 'Inspection ID,DBA Name,AKA Name,License #,Facility Type,Risk,Address,City,State,Zip,Inspection Date,Inspection Type,Results,Violations,Latitude,Longitude,Location' 
    if re.search(keyRE, row) :
        return 'singleline'
    keyRE = r'' # re to match '| list of violations'
    if re.search(keyRE, row) :
        return 'cont'
    keyRE = r'' # re to match all white space
    if re.search(keyRE, row) :
        return 'blank'
    keyRE = r'' # re to match serious violation
    if re.search(keyRE, row) :
        return 'serious'
    keyRE = r'' # re to match other no comma
    if re.search(keyRE, row) :
        return 'nocomma'
    print 'Unknown Row Type', row 
    return 'unknown'
def main():
"""
attempts to analyse a huge block of data on Chicago area restaurants.
"""
# define variables
    chiDict ={}
# read the whole file
    with open('data\food.csv', 'r') as csvfile:
        # Parse based on csv lib
        chiData = csv.reader( csvfile )
        for row in chiData:
            #Each row read from the csv file is returned as a list of strings. No automatic data type conversion is performed.
            # try a regular expression match to a pattern
            rowType = typeOfLine(row)
            #if it works process data
            if rowType == 'singleline':
                # process a single line
                None
            elif rowType == 'cont':
                # process a continuation
                None
            elif rowType == 'blank':
                # do nothing its a blank line
                None
            elif rowType == 'serious' :
                # handle these weird all text rows created for serious violations
                None
            #else try the alternate patterns
            #for debuging purposes we will print fall through cases

# call sorting functions that call the plotting functions

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__'
    main()