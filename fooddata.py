#!/usr/bin/python
# Analyse Chicago's food inspection data
# and make a series of tasty pie charts and tables
#  Outcomes of a health-inspection (pass, fail)
#  Risk levels
#  Breakdown of establishment types
#  Most common code violations
import csv
# import matplotlib
import re

def makeChart(subsetDict):
    """Takes a dictionary with the subset of data that we want and makes a chart """ 
    label_list = [subsetDict.keys() ]  #turns keys int a a list
    wedges = [subsetDict[x] for x in subsetDict.keys()] # turns data into a list with the same order
    matplotlib.pyplot.pie (  wedges, labels=label_list)
    matplotlib.pyplot.show()
    return None

def inspectionResults(foodDict) :
    """This makes a very basic pie chart that shows how often eateries pass inspection  """  
    # pull out inspection data
    iDict = {}
    return makeChart(iDict)

def commonViolationsChart(foodDict):
    """Prints a pie chart demonstrating the most common violations of health code cited """    
    # pull out violation data
    return makeChart(vDict)

def restaurantsTypes(foodDict):
    """Prints a pie chart demonstrating the proportions of restaurant types"""    
    # pull out restaurant type data
    return makeChart(rDict)

def additonalViolations(struct, row):
    """
    This function will take a uncommitted data structure of an inspection line
    and add its continuation to the violations list.
    """
    # for vitem in struct['Violations']:
        # print len(struct['Violations']), vitem[-40:]
    # for  vitem in violationsToList(row) :
        # print "to add:" , vitem[-40:]
    struct['Violations'] += violationsToList(row) 
    # for vitem in struct['Violations']:
        # print len(struct['Violations']), vitem[-40:]
    return struct
    
def violationsToList(str):
        """
        Takes a string violations and converts that to a list.
        """
        violations = list()
        numberToken = '([\d]+\.\s+)' #fixed to require 1 digit AND a dot
        matchshitck = re.search(numberToken ,str)

        while str and matchshitck: # while there are still tokens on the list 
            secondPlace = re.search(numberToken ,str[matchshitck.end(1):])
            if secondPlace :
                token = str[matchshitck.start(1):matchshitck.end(1) + secondPlace.start(1)] # take the first token fixed to get right endpoint
                #print "token:", token[:20], '...' , token[-20:]
                str = str[secondPlace.start(1) + matchshitck.end(1):] # cut off the last entry
                matchshitck = re.search(numberToken ,str) #because there is a secondPlace its there I just run the command to find it.
                violations.append(token) #add this token to the list.
            else:
                violations.append(str) # if there is no more append the remaining text as the last in list.
                matchshitck = None
        return violations
        
def relativeRisk(foodDict):
    """makes a bar chart comparing the violation percentage by restaurant type"""
    #for each violation keep of tally of the associated restaurant type
    #compare to the total number restaurants in that type

def typeOfLine(row):
    """this csv has many types of rows thrown together.  This fuction returns the type of row."""
    keyRE = '\d+' 
    # re to match 'Inspection ID,DBA Name,AKA Name,License #,Facility Type,Risk,Address,City,State,Zip,Inspection Date,Inspection Type,Results,Violations,Latitude,Longitude,Location' 
    if re.match(keyRE, row.split(',')[0]) :
        return 'singleline'
    keyRE = r' | ' # re to match '| list of violations'
    if keyRE == row[:3] or row[0] == '#':
        return 'cont'
    keyRE = r'^\s*$' # re to match all white space
    if re.match(keyRE, row) :
        return 'blank'
    if ('serious' in row.lower()) or ('critical' in row.lower()):
        if ('violation' in row.lower()) or ('citation' in row.lower()):
            return 'serious'
    keyRE = r',' # re to match other no comma
    if not re.search(keyRE, row) :
        return 'nocomma'
    #print 'Unknown Row Type'
    return 'unknown'

def singlelineToDict(row):
    """ 
    takes a row already IDed to be a single row and returns a dict with matching labels and data for that row.
    input is single row format:
    Inspection ID,DBA Name,AKA Name,License #,Facility Type,Risk,Address,City,State,Zip,Inspection Date,Inspection Type,Results,Violations,Latitude,Longitude,Location
    """
    returnable = dict() # create the dictionary that will later be returned.
    hackedrow = row.split(',') #break row on comma
    #
    #next we create a loop to build the returnable dict
    #
    labelspart1 = ['InspectionID','DBAName', 'AKAName', 'License' , 'FacilityType', 'Risk', 'Address', 'City', 'State', 'Zip', 'InspectionDate', 'InspectionType', 'Results']
    labelspart2 = [ 'Latitude', 'Longitude']
    # assign and remove the first remaining datum in the hackedrow to the first remaining label which will also be removed
    while labelspart1: # handle everything before the weird results sections
        returnable[ labelspart1.pop(0)] = hackedrow.pop(0)
    #location is actually the last 2 values
    returnable['Location'] = hackedrow[-2] + ',' + hackedrow[-1]
    hackedrow.pop(-1)
    hackedrow.pop(-1)
    while labelspart2: # handle everything after the weird results sections
        returnable[ labelspart2.pop(-1)] = hackedrow.pop(-1)
    #dump the rest of hackedrow into results entry for violations
    hackedrow_results = hackedrow.pop(0)
    while hackedrow:
        hackedrow_results += ',' + hackedrow.pop(0)
    returnable['Violations' ] = hackedrow_results
    return returnable

def seriousRowDecoder(row):
    """
    Works to break down serious violation rows from a huge block of data on Chicago area restaurants.
    input format "SERIOUS VIOLATION: 7-42-090" or 'SERIOUS CITATION ISSUED: 7-42-090' or 'CRITICAL VIOLATION 7-42-090 CITATION ISSUED.'
    inconsistent inputs really make this more complex
    """
    seriousDict = dict() # a small dictionary decoding the line
    token = re.search(r'([\d-]+)',row) #find the code number and load it into token.group(1)
    if token:
        seriousDict['number'] = token.group(1)
    else:
        print 'code number detection has failed in seriousRowDecoder'
    lcrow = row.lower()
    # because of inconsistent format a word search seems like the best option to get a good label
    if 'serious' in lcrow:
        if 'citation' in lcrow:
            seriousDict['label'] = 'SERIOUS CITATION'
        elif 'violation' in lcrow:
            seriousDict['label'] = 'SERIOUS VIOLATION'
    elif 'critical' in lcrow:
        if 'citation' in lcrow:
            seriousDict['label'] = 'CRITICAL CITATION'
        elif 'violation' in lcrow:
            seriousDict['label'] = 'CRITICAL VIOLATION'
    return seriousDict
    
def main():
    """
    attempts to analyse a huge block of data on Chicago area restaurants.
                    # Handle multiline logg etries
                # Split off which establishment these rows correspond to
                # add to the chiDict entry for that establishment
                # create a list of serious violations per establishment 
                # work through next line and link to continuation code if applicable 
                #   That work flow for a multi line comment should be something link this pseudo-code
                #   ID 1st line of serious violation
                #   call a function that takes the first line and breaks it down into a good data structure 'buffer'.
                #   loop
                #   process the next line.
                #   if its not a continuation, 
                #       commit the buffer to the dictionary
                #       blank the 'buffer' signalling that there is nothing to commit next cycle
                #       process the line normally
                #   else,
                #       call a function to add the continuation to the buffer
                #   go to loop if buffer not blank

    """
    # define variables
    chiDict =dict()
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
                # add the dictionary of data from the single to the larger dictionary of data.
                # commit working data 
                singlelineDict = singlelineToDict(row)
                if not singlelineDict['License'] in chiDict.keys():
                    # I should split up violations into a more useful data structure.
                    chiDict[ singlelineDict['License']] = singlelineDict
                else:
                    # add to existing data
                    None
                None
            elif rowType == 'serious':
                seriousDict = seriousRowDecoder(row)
                # add this to the serious violations database and add it to the appropriate entry in the main database
                None
            elif rowType == 'blank':
                # do nothing its a blank line
                None
            elif rowType == 'cont' :
                # process a continuation
                None
            #else try the alternate patterns
            #for debuging purposes we will print fall through cases

# call sorting functions that call the plotting functions

# Standard boilerplate to call the main() function to begin
# the program.
# if __name__ == '__main__'
    # main()