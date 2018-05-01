# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: Script for analyzing SQL voter file, e.g. calculate correlations, do linear regressions, etc


import MySQLdb, numpy, sys
from voterFileSQL import *
from sys import argv

#  0. ***  Do some parsing for username and passwd --> should really use argparse
opts = {}  
while argv: 
    if argv[0][0] == '-':  # Found a "-name value" pair.
        opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
    argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.

if '-u' not in opts.keys() or '-p' not in opts.keys():
    print 'Script requires -u <username> and -p <passwd> inputs in order to access SQL DB\n===============\nEXITING===============\n'
    sys.exit()


#  1. ***  Connect to SQL database
print opts['-u'], opts['-p']
db = MySQLdb.connect(host="lenin.party",  # your host 
                     user=opts['-u'],     # username
                     passwd=opts['-p'],   # password
                     db="voter_ohio")     # name of the database

#connection = sqlite3.connect("../sql/voterFile.db")
#db.create_aggregate("stdev", 1, StdevFunc)
cursor = db.cursor()

# move to correct table
cursor.execute("SHOW TABLES")
cursor.execute("USE VOTER_OHIO")
cursor.execute("SHOW TABLES")
cursor.execute("DESCRIBE franklin_raw_20171231")

for row in cursor.fetchall() :
    print row[0], " ", row[1]

cursor.execute("SELECT * FROM franklin_raw_20171231 LIMIT 3, 6")
for row in cursor.fetchall() :
    print row
    #print row[0], " ", row[1]

sys.exit()

# Select data from table using SQL query.
cursor.execute("SELECT * FROM franklin_raw_20171231")
 
# print the first and second columns      
for row in cursor.fetchall() :
    print row[0], " ", row[1]

sys.exit()
#  1. ***  Print some simple summaries
#printSimpleSummary(cursor)
printSimpleSummary(cursor, subsample='0')

sys.exit()

#  2. ***  Calculate some correlations
#calculateCorrelation(cursor, 'P_052014 v G_112014', ['P_052014', 'G_112014'])
#calculateCorrelation(cursor, 'P_052014 v G_112014 (Active)', ['P_052014', 'G_112014'], constraints="STATUS like 'A'")
#calculateCorrelation(cursor, 'P_052014 v G_112014 (G0)', ['P_052014', 'G_112014'], subsample='0')
#calculateCorrelation(cursor, 'P_052014 v G_112014 (Active, G0)', ['P_052014', 'G_112014'], "STATUS like 'A'", subsample='0')
#calculateCorrelation(cursor, 'P_052014 v G_112014 (Active, G0, Registered 2010)', ['P_052014', 'G_112014'], "STATUS like 'A' and REGISTERED <= Datetime('2014-05-01 00:00:00')", subsample='0')
             

#  3. ***  Calculate Bayesian probabilities
print '================================================================================='
print '===============        Calculating Bayesian Probabilities         ==============='
print '================================================================================='
##   i. ** Relate general election to that year's primary  
#returnBayesianProbability(cursor, 'P( G_112012 | P_032012 ) [Active, Reg, G0]', ['G_112012', 'P_032012'], "STATUS like 'A' and REGISTERED <= Datetime('2012-03-01 00:00:00')", subsample='0') 
#returnBayesianProbability(cursor, 'P( G_112015 | P_052015 ) [Active, Reg, G0]', ['G_112015', 'P_052015'], "STATUS like 'A' and REGISTERED <= Datetime('2015-05-01 00:00:00')", subsample='0') 
#returnBayesianProbability(cursor, 'P( G_112016 | P_032016 ) [Active, Reg, G0]', ['G_112016', 'P_032016'], "STATUS like 'A' and REGISTERED <= Datetime('2016-03-01 00:00:00')", subsample='0') 

##   ii. ** Use automated function to get average relation and stdev
"""returnBayesianRelation(cursor, 'Voted In General | Voted In Same-Year Primary', ['G', 'P'], yearGap=0, voted=True, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Did Not Vote In Same-Year Primary', ['G', 'P'], yearGap=0, voted=False, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Voted In Previous-Year General', ['G', 'G'], yearGap=1, voted=True, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Did Not Vote In Previous-Year General', ['G', 'G'], yearGap=1, voted=False, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Voted In Previous-Year Primary', ['G', 'P'], yearGap=1, voted=True, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Did Not Vote In Previous-Year Primary', ['G', 'P'], yearGap=1, voted=False, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Voted In 2 Years Previous Primary', ['G', 'P'], yearGap=2, voted=True, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Did Not Vote In 2 Years Previous Primary', ['G', 'P'], yearGap=2, voted=False, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Voted In 2 Years Previous General', ['G', 'G'], yearGap=2, voted=True, constraints="STATUS like 'A'", subsample='0', quiet=True)
returnBayesianRelation(cursor, 'Voted In General | Did Not Vote In 2 Years Previous General', ['G', 'G'], yearGap=2, voted=False, constraints="STATUS like 'A'", subsample='0', quiet=True)
"""

norm = returnBayesianProbability(cursor, 'P( G_112015 | P_052015 ) [Active, Reg, G0]', ['G_112015', 'P_052015'], "STATUS like 'A' and REGISTERED <= Datetime('2015-05-01 00:00:00')", subsample='0') 
new = returnBayesianHistory(cursor, 'test', ['G_112015', 'P_052015'], [1,1], constraints="STATUS like 'A' and REGISTERED <= Datetime('2015-05-01 00:00:00')", subsample='0', quiet=False)
add = returnBayesianHistory(cursor, 'test', ['G_112015', 'P_052015', 'G_112014'], [1,1,1], constraints="STATUS like 'A' and REGISTERED <= Datetime('2014-11-01 00:00:00')", subsample='0', quiet=False)
add2 = returnBayesianHistory(cursor, 'test', ['G_112015', 'P_052015', 'G_112014'], [-1,1,1], constraints="STATUS like 'A' and REGISTERED <= Datetime('2014-11-01 00:00:00')", subsample='0', quiet=False)

print norm, new, add, add2
