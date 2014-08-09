#!/usr/bin/python
# Analyse Chicago's food inspection data
# and make a series of tasty pie charts and tables
#  Outcomes of a health-inspection (pass, fail)
#  Risk levels
#  Breakdown of establishment types
#  Most common code violations
import csv
# import matplotlib # forget matplotlib I'm going to use https://developers.google.com/chart as no install is required
import re
import os.path # used by makeChart to create new unnamed charts 
import webbrowser # used by makeChart to open the freshly created chart.

def makeChart(chartableDict):
    """Takes a dictionary with the subset of data that we want and makes a chart 
    Input : chartableDict which can have special entries 
        "control chart title" => the title of the new chart,
            if absent or blank title will be 'chart title'
        "control chart options" => the options to be sent to google charts, 
            if absent or blank defaults will be used
        all other keys are labels for the new chart, and correspond to data points.
        'control open chart' => if present indicates chart should open automatically
    Output: a file named whatever the chartableDict['control chart title'] + '.html',
        or, if absent or blank, chart\d+.html w/ \d+ as lowest possible choice starting at zero
    """ 
    htmlPriorToChart = """<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Label', 'Data'],"""
    htmlFollowingChart = """
        var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="piechart_3d" style="width: 900px; height: 500px;"></div>
  </body>
</html>
    """
    controlOpenChart = None #thus it does not open by default
    controlChartTitle = ''# title of chart
    controlChartOptions = '' # the options properly formatted to be loaded into the HTML file
    htmlDataChart = '' # the working string of html of chart data 
    # check for control chart title and set it
    if 'control open chart' in chartableDict.keys():
        controlOpenChart = chartableDict['control open chart']
        del chartableDict['control open chart']
    if 'control chart title' in chartableDict.keys() :
        if chartableDict['control chart title']:
            controlChartTitle = chartableDict['control chart title'] # load it into controlChartTitle
        else:
            chartNumber = 1
            while chartNumber :
                if not os.path.isfile('chart' + str(chartNumber - 1) + '.html' ):
                    controlChartTitle = 'chart' + str(chartNumber - 1) + '.html'
                    chartNumber = 0
                else:
                    chartNumber += 1
        del chartableDict['control chart title'] # remove control key
    else:    
        # if absent or blank pick first available generic chart name
        chartNumber = 1
        while chartNumber :
            if not os.path.isfile('chart' + str(chartNumber - 1) + '.html' ):
                controlChartTitle = 'chart' + str(chartNumber - 1) + '.html'
                chartNumber = 0
            else:
                chartNumber += 1
    # create the options strings from control chart options
    if 'control chart options' in chartableDict.keys():
        if chartableDict['control chart options'] :
            controlChartOptions = chartableDict['control chart options']
        del chartableDict['control chart options'] # remove control key
    else:
        None # leave it blank
     # for each key remaining treat them as a label 
    for datum in chartableDict.keys():
        # add a label and data row to the htmlDataChart
        if htmlDataChart:
            htmlDataChart +=',' # if its not blank put a comma at the end, saves unneeded trailing comma         
        if datum.find("'") + 1 : # fix raw ' in labels 
            fixed_datum = datum
            fixed_datum = fixed_datum.replace("'","feet")
            htmlDataChart += "\n          ['" + fixed_datum  + "',   " + str(chartableDict[datum]) + '  ]' 
        else: 
            htmlDataChart += "\n          ['" + str(datum) + "',   " + str(chartableDict[datum]) + '  ]' 
    htmlDataChart += '\n        ]);\n'    #close chart
    # write all 4 parts of HTML to the file.
    f = open( controlChartTitle ,'w')
    f.write(htmlPriorToChart)
    f.write(htmlDataChart)
    f.write(controlChartOptions)
    f.write(htmlFollowingChart)
    f.close()
    if controlOpenChart:
        webbrowser.open_new_tab(controlChartTitle) # call web browser to open html file.
    return None

def inspectionResults(foodDict) :
    """This makes a very basic pie chart that shows how often eateries pass inspection  """  
    # pull out chart data
    iDict = {}
    if 'control open chart' in foodDict:
        iDict['control open chart'] = foodDict ['control open chart']
        del foodDict ['control open chart']
    if 'control chart title' in foodDict:
        iDict['control chart title'] = foodDict ['control chart title']
        del foodDict ['control chart title']
    if 'control chart options' in foodDict:
        iDict['control chart options'] = foodDict ['control chart options']
        del foodDict ['control chart options']
    for i in foodDict.keys() : # for each inspection 
        if foodDict[i]['Results'] in iDict.keys(): #If the result is in the dict
            iDict[ foodDict[i]['Results'] ] += 1 # increase the tally
        else:
            iDict[ foodDict[i]['Results'] ] = 1 # start a new tally
    return makeChart(iDict)

def commonViolationsChart(foodDict):
    """Prints a pie chart demonstrating the most common violations of health code cited """    
    chartDictSize = 6
    vDict = dict() # working tally of voilations by number
    xrefernce = dict() # crossreference of violation number and human readable name
    chartableDict = dict() # most common 5 violations for pie chart
    sortViolations = list() # a sortable list of touples.
    vNumberPattern =  '([\d]+)\.\s+'
    if 'control open chart' in foodDict:
        chartableDict['control open chart'] = foodDict ['control open chart']
        chartDictSize += 1
        del foodDict ['control open chart']
    if 'control chart title' in foodDict:
        chartDictSize += 1
        chartableDict['control chart title'] = foodDict ['control chart title']
        del foodDict ['control chart title']
    if 'control chart options' in foodDict:
        chartDictSize += 1
        chartableDict['control chart options'] = foodDict ['control chart options']
        del foodDict ['control chart options']
    # pull out violation data
    for i in foodDict.keys() : # for each inspection 
        for violation in foodDict[i]['Violations']:
            rev = re.search(vNumberPattern, violation)
            violationNumber = rev.group(1)
            if violationNumber in vDict.keys(): #If the result is in the dict
                vDict[ violationNumber ] += 1 # increase the tally
            else:
                vDict[ violationNumber ] = 1 # start a new tally
                #create a working xrefernce table for better labels
                xrefernce [violationNumber] = violation
    def lastest(l): return l[-1]  # inline function defined
    for i in vDict.keys():
        sortViolations.append( (xrefernce[i] , vDict[i]) )
    if len(sortViolations) <= chartDictSize: # if there is not enough data to need to cut some off.
        while sortViolations:
            violation, tally = sortViolations.pop(0) 
            chartableDict[violation] = tally  
        return makeChart(chartableDict)
    sortViolations = sorted(sortViolations, key=lastest, reverse = True) # gives a sorted list touples starting with the biggest
    while len(chartableDict) < chartDictSize: # will build up the final list of violation data
        violation, tally = sortViolations.pop(0) 
        chartableDict[violation] = tally  
    return makeChart(chartableDict)

def restaurantsTypes(foodDict):
    """Prints a pie chart demonstrating the proportions of restaurant types"""    
    rDict = dict()
    if 'control open chart' in foodDict:
        rDict['control open chart'] = foodDict ['control open chart']
        del foodDict ['control open chart']
    if 'control chart title' in foodDict:
        rDict['control chart title'] = foodDict ['control chart title']
        del foodDict ['control chart title']
    if 'control chart options' in foodDict:
        rDict['control chart options'] = foodDict ['control chart options']
        del foodDict ['control chart options']
    for i in foodDict.keys() : # for each inspection 
        if re.search('\S',foodDict[i]['FacilityType']): # has non-space characters
            if foodDict[i]['FacilityType'] in rDict.keys(): #If the 'FacilityType' is in the dict
                rDict[ foodDict[i]['FacilityType'] ] += 1 # increase the tally
            else:
                rDict[ foodDict[i]['FacilityType'] ] = 1 # otherwise start a new tally
    return makeChart(rDict)

def additonalViolations(struct, row):
    """
    This function will take a uncommitted data structure of an inspection line
    and add its continuation to the violations list.
    """
    struct['Violations'] += violationsToList(row) 
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
    """makes a pie chart comparing the violation percentage by restaurant type"""
    #for each violation keep of tally of the associated restaurant type
    #compare to the total number restaurants in that type
    rDict = dict()
    if 'control open chart' in foodDict:
        rDict['control open chart'] = foodDict ['control open chart']
        del foodDict ['control open chart']
    if 'control chart title' in foodDict:
        rDict['control chart title'] = foodDict ['control chart title']
        del foodDict ['control chart title']
    if 'control chart options' in foodDict:
        rDict['control chart options'] = foodDict ['control chart options']
        del foodDict ['control chart options']
    for i in foodDict.keys() : # for each inspection 
        if re.search('\S',foodDict[i]['Risk']): # has non-space characters
            if foodDict[i]['Risk'] in rDict.keys(): #If the 'Risk' is in the dict
                rDict[ foodDict[i]['Risk'] ] += 1 # increase the tally
            else:
                rDict[ foodDict[i]['Risk'] ] = 1 # otherwise start a new tally
    return makeChart(rDict)

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
    Now lists violations and upper case all data due to inconsistent data entry
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
        returnable[ labelspart1.pop(0)] = hackedrow.pop(0).upper()
    #location is actually the last 2 values
    returnable['Location'] = hackedrow[-2] + ',' + hackedrow[-1]
    hackedrow.pop(-1)
    hackedrow.pop(-1)
    while labelspart2 and hackedrow: # handle everything after the weird results sections
        returnable[ labelspart2.pop(-1)] = hackedrow.pop(-1)
    #dump the rest of hackedrow into results entry for violations
    if hackedrow: # handles the possible case of 0 violations 
        hackedrow_results = hackedrow.pop(0)
    else:
        hackedrow_results = ''
    while hackedrow:
        hackedrow_results += ',' + hackedrow.pop(0)
    returnable['Violations' ] = violationsToList(hackedrow_results)
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
    chiDict =dict() # the large dictionary of all lines processed
    workingDict = dict() #the current working file before committing to chiDict
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
                if not workingDict['InspectionID'] in chiDict.keys():
                    # I should split up violations into a more useful data structure.
                    chiDict[ workingDict['InspectionID']] = workingDict
                else:
                    # add to existing data
                    None
                workingDict = singlelineToDict(row)   
            elif rowType == 'serious':
                seriousDict = seriousRowDecoder(row)
                # add this to the serious violations database and add it to the appropriate entry in the main database
                None
            elif rowType == 'blank':
                # do nothing its a blank line
                None
            elif rowType == 'cont' :
                workingDict = additonalViolations(workingDict, row)
                None
            #else try the alternate patterns
        if workingDict : # if there is uncommitted data
            None
            # add the dictionary of data remaining to the larger dictionary of data. 

# call sorting functions that call the plotting functions

# Standard boilerplate to call the main() function to begin
# the program.
# if __name__ == '__main__'
    # main()