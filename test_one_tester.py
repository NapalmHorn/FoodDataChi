import unittest
from fooddata import typeOfLine, singlelineToDict, makeChart
# import fuctions for testing
#import testFunction from testFile # replace with the name of your file and fuctions
#to test simply run 'python boilerplatetester.py'

class oneFuntionTester(unittest.TestCase):

    def test_show_failing_lines(self):
        rowsRead = rowFalures = 0 
        #read the file
        csvfile = open('food.csv', 'r')
        row = csvfile.readline()
        while row: #for each line
            rowsRead += 1 # increment line counter
            rowType = typeOfLine(row) #test what time of line
            if rowType == 'singleline': # try to decode the line
                if not singlelineToDict(row):
                    rowFalures += 1
            row = csvfile.readline()
        # if it fails to encode increment failure counter 
        # make a chart of the successes and failures 
        testCase = dict()
        testCase["control open chart"] = True
        testCase["control chart title"] = 'RowRead.htm'
        testCase["control chart options"] = """
        var options = {
          title: 'Self test of the validity of row reads ',
          is3D: true,
          colors:['red','green']
        };
        """
        testCase['Bad Reads'] = rowFalures
        testCase['Good Reads'] = rowsRead - rowFalures
        makeChart(testCase)
    
if __name__ == '__main__':
    unittest.main()