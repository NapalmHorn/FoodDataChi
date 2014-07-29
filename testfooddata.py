import unittest
from fooddata import typeOfLine  
#from testFile import testFunction
#to test simply run 'python boilerplatetester.py'

class boilerplateTestCase(unittest.TestCase):
    def test_single_good_line(self): #
        """ should succeed and demonstrates that typeOfLine can find a good single line log entry """
        expectedResult = 'singleline'
        testCase = '99888,ROOK CAFE AND SMOOTHIE BAR,ROOK CAFE AND SMOOTHIE BAR,2188890,'
        testCase += 'Restaurant,Risk 2 (Medium),816 S MICHIGAN AVE ,CHICAGO,IL,60605,03/06/2013,Complaint,Fail,'
        testCase += '"1. SOURCE SOUND CONDITION, NO SPOILAGE, FOODS PROPERLY LABELED, SHELLFISH TAGS IN PLACE - '
        testCase += 'Comments: UNAPPROVED SOURCE:FOUND 10 BUTTER COOKIES ON COUNTER FOR SALE WITHOUT PROPER LABELING AND NO INVOICE TO SHOW COOKIES COME FROM AN APPROVED SOURCE. INSTRUCTED TO PROVIDE/HAVE ON PREMISES AT ALL TIMES. CRITICAL VIOLATION 7-38-005(B) | 3. POTENTIALLY HAZARDOUS FOOD MEETS TEMPERATURE REQUIREMENT DURING STORAGE, PREPARATION DISPLAY AND SERVICE - Comments: FOUND A CONTAINER OF ITALIAN BEEF AT AN IMPROPER TEMPERATURE-55.3F, STORED IN THE REACH IN COOLER. ITEM WAS DISCARDED, 2LBS. VALUED AT $20.OO. INSTRUCTED TO KEEP POTENTIALLY HAZARDOUS FOODS AT 40F OR LOWER. CRITICAL VIOLATION 7-38-005(A) | 9. WATER SOURCE: SAFE, HOT & COLD UNDER CITY PRESSURE - Comments: FOUND NO HOT WATER PER CITY CODE ON THE PREMISES. INSTRUCTED TO HAVE HOT WATER ON THE PREMISES AT ALL TIMES. CRITICAL VIOLATION 7-38-030 | 35. WALLS, CEILINGS, ATTACHED EQUIPMENT CONSTRUCTED PER CODE: GOOD REPAIR, SURFACES CLEAN AND DUST-LESS CLEANING METHODS - Comments: MUST REPLACE WATER STAINED CEILING IN DINING AREA. | 41. PREMISES MAINTAINED FREE OF LITTER, UNNECESSARY ARTICLES, CLEANING  EQUIPMENT PROPERLY STORED - Comments: MUST ELIMINATE ALL UNNECESSARY ARTICLES IN PREP AREA AND ORGANIZE AREA. | 32. FOOD AND NON-FOOD CONTACT SURFACES PROPERLY DESIGNED, CONSTRUCTED AND MAINTAINED - Comments: MUST PROVIDE A SNEEZE GUARD OVER HOT HOLDING FOOD ITEMS ON THE FRONT COUNTER. | 38. VENTILATION: ROOMS AND EQUIPMENT VENTED AS REQUIRED: PLUMBING: INSTALLED AND MAINTAINED - Comments: MUST FIX SLOW DRAINING 3-COMP. SINK IN PREP AREA.",41.87162384657216,-87.62431054852696,"(41.87162384657216, -87.62431054852696)"'
        self.assertTrue(typeOfLine(testCase) == expectedResult)
    
    def test_single_bad_line(self):
        """ should not succeed and demonstrates that typeOfLine will not pass everything close to a single line entry"""
        expectedResult = 'singleline'
        testCase = 'VODKA IS YUMMY,ROOK CAFE AND SMOOTHIE BAR,a;lsdka;lskdjflkajsdfoiajwe;ncajwehi;ef"1. SOURCE SOUND CONDITION, NO SPOILAGE, FOODS PROPERLY LABELED, SHELLFISH TAGS IN PLACE - Comments: UNAPPROVED SOURCE:FOUND 10 BUTTER COOKIES ON COUNTER FOR SALE WITHOUT PROPER LABELING AND NO INVOICE TO SHOW COOKIES COME FROM AN APPROVED SOURCE. INSTRUCTED TO PROVIDE/HAVE ON PREMISES AT ALL TIMES. CRITICAL VIOLATION 7-38-005(B) | 3. POTENTIALLY HAZARDOUS FOOD MEETS TEMPERATURE REQUIREMENT DURING STORAGE, PREPARATION DISPLAY AND SERVICE - Comments: FOUND A CONTAINER OF ITALIAN BEEF AT AN IMPROPER TEMPERATURE-55.3F, STORED IN THE REACH IN COOLER. ITEM WAS DISCARDED, 2LBS. VALUED AT $20.OO. INSTRUCTED TO KEEP POTENTIALLY HAZARDOUS FOODS AT 40F OR LOWER. CRITICAL VIOLATION 7-38-005(A) | 9. WATER SOURCE: SAFE, HOT & COLD UNDER CITY PRESSURE - Comments: FOUND NO HOT WATER PER CITY CODE ON THE PREMISES. INSTRUCTED TO HAVE HOT WATER ON THE PREMISES AT ALL TIMES. CRITICAL VIOLATION 7-38-030 | 35. WALLS, CEILINGS, ATTACHED EQUIPMENT CONSTRUCTED PER CODE: GOOD REPAIR, SURFACES CLEAN AND DUST-LESS CLEANING METHODS - Comments: MUST REPLACE WATER STAINED CEILING IN DINING AREA. | 41. PREMISES MAINTAINED FREE OF LITTER, UNNECESSARY ARTICLES, CLEANING  EQUIPMENT PROPERLY STORED - Comments: MUST ELIMINATE ALL UNNECESSARY ARTICLES IN PREP AREA AND ORGANIZE AREA. | 32. FOOD AND NON-FOOD CONTACT SURFACES PROPERLY DESIGNED, CONSTRUCTED AND MAINTAINED - Comments: MUST PROVIDE A SNEEZE GUARD OVER HOT HOLDING FOOD ITEMS ON THE FRONT COUNTER. | 38. VENTILATION: ROOMS AND EQUIPMENT VENTED AS REQUIRED: PLUMBING: INSTALLED AND MAINTAINED - Comments: MUST FIX SLOW DRAINING 3-COMP. SINK IN PREP AREA.",41.87162384657216,-87.62431054852696,"(41.87162384657216, -87.62431054852696)"'
        self.assertTrue(typeOfLine(testCase) != expectedResult)
    
    def test_blank_good_line(self): #
        """ should succeed and demonstrates that typeOfLine can find and id a blank line log entry """
        expectedResult = 'blank'
        testCase = ' '
        self.assertTrue(typeOfLine(testCase) == expectedResult)
    
    def test_blank_bad_line(self): #
        """ should fail and demonstrates that typeOfLine can find and id a blank line log entry """
        expectedResult = 'blank'
        testCase = ' . '
        self.assertTrue(typeOfLine(testCase) != expectedResult)
    
    def test_cont_good_line(self): #
        """ should fail and demonstrates that typeOfLine can find and id a blank line log entry """
        expectedResult = 'cont'
        testCase = ' | 35. WALLS, CEILINGS, ATTACHED EQUIPMENT CONSTRUCTED PER CODE: GOOD REPAIR, SURFACES CLEAN AND DUST-LESS CLEANING METHODS - Comments: WALLS AROUND 3 COMPARTMENT SINK IN NEED OF CLEANING TO REMOVE SPLATTER. '
        self.assertTrue(typeOfLine(testCase) == expectedResult)
    
    def test_serious_good1_line(self): #
        """ should succeed and demonstrates that typeOfLine can find and id a serious (critical) violation (citation) line log entry 1st case """
        expectedResult = 'serious'
        testCase = 'SERIOUS VIOLATION 7-38-012 CITATION ISSUED'
        self.assertTrue(typeOfLine(testCase) == expectedResult)
    
    def test_serious_good2_line(self): #
        """ should succeed and demonstrates that typeOfLine can find and id a serious (critical) violation (citation) line log entry 2nd case"""
        expectedResult = 'serious'
        testCase = 'CRITICAL CITATION ISSUED: 7-38-005 (A) \| 3. POTENTIALLY HAZARDOUS FOOD MEETS TEMPERATURE REQUIREMENT DURING STORAGE, PREPARATION DISPLAY AND SERVICE - Comments: OBSERVED PREPARED COOKED FOODS IN DISPLAY COOLER CASE READING AT IMPROPER TEMP., READING BETWEEN 48.7-50.1\'F, ALL PRODUCT DUMPED AND DENATURE AT A COST OF ABOUT $676.00, AND ABOUT 181.60 POUNDS, INSTRUCTED MANAGER THAT PIZZA THATS READING 29\'F, CAN BE SOLD, BUT NOT REFROZEN, MANAGER DECIDED TO DISCARD PIZZA, AT A COST OF ABOUT $889.20, AND ABOUT 275 POUNDS, SEE ATTACHED INVOICES AND RECEIPTS, '
        self.assertTrue(typeOfLine(testCase) == expectedResult)
        
    def test_serious_good3_line(self): #
        """ should succeed and demonstrates that typeOfLine can find and id a serious (critical) violation (citation) line log entry 3rd case"""
        expectedResult = 'serious'
        testCase = 'SERIOUS CITATION ISSUED: 7-38-020 | 33. FOOD AND NON-FOOD CONTACT EQUIPMENT UTENSILS CLEAN, FREE OF ABRASIVE DETERGENTS - Comments: MUST DETAIL CLEAN: TOPS AND SIDE OF COOKING EQUIPMENT, VENTS ABOVE COOKING EQUIPMENT, VENTS ABOVE DISH MACHINES NOT CLEAN, AND EXTERIOR SURFACES OF BULK CONTAINERS, AT BOTH PREP AREAS, 1ST AND 2ND FLOORS, MUST DETAIL CLEAN ALL SURFACES | 32. FOOD AND NON-FOOD CONTACT SURFACES PROPERLY DESIGNED, CONSTRUCTED AND MAINTAINED - Comments: MUST PROVIDE SPLASH GUARDS AT EXPOSED HAND SINKS AT BAR AREAS, BETWEEN COUNTER AREA AND THREE COMPARTMENT SINKS | 34. FLOORS: CONSTRUCTED PER CODE, CLEANED, GOOD REPAIR, COVERING INSTALLED, DUST-LESS CLEANING METHODS USED - Comments: FLOORS THROUGHOUT PREMISES, UNDER AND BEHIND ALL EQUIPMENT, ON ALL FLOORS NEEDS DETAILED CLEANING, AND RESTRICT STORING ARTICLES ON FLOOR, MUST BE 6 INCHES FROM FLOOR AND WALL | 35. WALLS, CEILINGS, ATTACHED EQUIPMENT CONSTRUCTED PER CODE: GOOD REPAIR, SURFACES CLEAN AND DUST-LESS CLEANING METHODS - Comments: WALL SECOND FLOOR STORAGE AREA NEEDS SEALED, TO REMOVE ALL DUSTY BRICK PARTICLES FROM COMING OFF OF WALL, SURFACES MUST BE SMOOTH AND EASILY CLEANABLE | 36. LIGHTING: REQUIRED MINIMUM FOOT-CANDLES OF LIGHT PROVIDED, FIXTURES SHIELDED - Comments: MUST INCREASE LIGHT IN FIRST FLOOR KITCHEN PREP AND DISH AREA, LIGHT TOO DIM | 37. TOILET ROOM DOORS SELF CLOSING: DRESSING ROOMS WITH LOCKERS PROVIDED: COMPLETE SEPARATION FROM LIVING/SLEEPING QUARTERS - Comments: PERSONAL ITEMS STORED IN BASEMENT, NOT STORED NEATLY, MUST BE ONE DESIGNATED AREA, NICE AND NEATLY | 41. PREMISES MAINTAINED FREE OF LITTER, UNNECESSARY ARTICLES, CLEANING  EQUIPMENT PROPERLY STORED - Comments: MUST CLEAN AND BETTER ORGANIZE, ALL STORAGE AREAS, REMOVE ALL CLUTTER, CLEAN AND BETTER MAINTAIN ALL AREAS, MUST ELEVATE ALL ARTICLES 6 INCHES FROM FLOOR AND WALL, AND PROVIDE SHELVING TO BETTER MAINTAIN",41.92353245816767,-87.69813956418868,"(41.92353245816767, -87.69813956418868)"'
        self.assertTrue(typeOfLine(testCase) == expectedResult)    
       
    def test_serious_bad_line(self): #
        """ should fail and demonstrates that typeOfLine can find and id a blank line log entry """
        expectedResult = 'serious'
        testCase = 'LABEL ALL FOODS WITH NAME AND DATE.",41.96846837763899,-87.69299972102974,"(41.96846837763899, -87.69299972102974)"'
        self.assertTrue(typeOfLine(testCase) != expectedResult)
    
if __name__ == '__main__':
    unittest.main()