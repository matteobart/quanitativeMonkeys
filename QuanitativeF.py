import csv
import numpy
import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random




#this function is able to pull stock data from an api
#the only problem is that it can hang
#returns a float
def getStock(name, year):
	if name == 0 or name.isalpha() != True: 
		return 0
	try:
		start = datetime.datetime(year, 12, 31)
		end = datetime.datetime(year+1, 1, 1)
		f = web.DataReader(name, 'morningstar', start, end)
		return f["Close"][1]
	except:
		print("Not avilable for " + name + " in year " + str(year))
		return 0;


missingPerYear = []



#creates the 3-d array
#[year][stock number][0|1] 0 = name | 1 = price
allSPXstocks = [[[0 for k in xrange(2)] for j in xrange(510)] for i in xrange(2011-1991)]
#run through all the years in the files 
#add it to the 3d array
for i in range(1991, 2011):
	f=open("/Users/MatteoBartalini/Desktop/SP2/Dec"+str(i)+".csv")
	reader=csv.reader(f)
	count = 0
	for row in reader:
		if (row[2]!="" and row[2]!="price"):
			allSPXstocks[i-1991][count][0] = row[0].replace(" US Equity", "").replace(" UW Equity", "").replace(" UQ Equity", "").replace(" UA Equity", "").replace(" UN Equity", "")
			allSPXstocks[i-1991][count][1] = row[2]
			count = count + 1

#our version of the SPX average
SAMP = [0 for i in xrange(2010-1990)] #for each year

#used to find the "average" of SPX
#add to SAMP
for i in range(1992, 2011):
	missingCount = 0
	yearAverages = [0 for k in xrange(510)] #temp data to help find the average
	for j in xrange(510):			
		name = allSPXstocks[i-1991][j][0]
		thisYear = float(allSPXstocks[i-1991][j][1])
		lastYear = 0
		for j1 in xrange(510): #run through last years stocks
			if(allSPXstocks[i-1992][j1][0]==name):
				lastYear = float(allSPXstocks[i-1992][j1][1])
		if (lastYear != 0 and thisYear!= 0): #if we have both pieces of info... find the y/y for that stock
			yearAverages.append((thisYear-lastYear)/lastYear)
		else:
			missingCount = missingCount + 1	
	missingPerYear.append(missingCount)

	#now lets calculate total for the year
	total = 0 #all stocks added
	c = 0 #count 
	for d in yearAverages:
		c = c + 1
		total = total + d
	SAMP[i-1991] = total / c #I think this should be 1991

SAMP = SAMP[1:20]


#prices of the spx [1990-i]
spxPrice = [] 


#adds data to spxPrice
f=open("/Users/MatteoBartalini/Desktop/SP/screen.csv")
reader = csv.reader(f)
grab = 12+119*12
for i, row in enumerate(reader):
	if i == grab:
		spxPrice.append(float(row[1])) 
		grab = grab + 12



spxYoY = []

#added the percent change to spxyoy
for i in range(1,20):
	spxYoY.append((spxPrice[i]-spxPrice[i-1])/spxPrice[i-1])




print("\n")
print("\n")

#find the average of each yoy 
#spx actual
print("Average year over year")
ra = 0
for i  in range(0, len(spxYoY)):
	ra = ra + spxYoY[i]
print("SPX:")
print(str(ra/len(spxYoY)))


#samp
rb = 0 
for i in range(0, len(SAMP)):
	rb = rb + SAMP[i]
print("SAMP:")
print(str(rb/len(SAMP)))


print("\n")
print("\n")



for i in range(0, len(spxYoY)):
	spxYoY[i] = 100 * spxYoY[i]

for i in range(0, len(SAMP)):
	SAMP[i] = 100 * SAMP[i]



print(len(ms))
print(len(SAMP))


#create the graph
df = pd.DataFrame({'x': range(1991, 2010), 'SAMP': SAMP, 'SPX': spxYoY, 'Market Skew': ms})
plt.plot('x', 'SAMP', data=df, linestyle="-", marker='o')
plt.plot('x', 'SPX', data=df, linestyle="-", marker='o')
plt.xticks(np.arange(1990, 2011, 4),)
plt.legend()
plt.ylabel("Year/Year Return (%)")
plt.xlabel("Year")
plt.title("SPX vs SAMP")
plt.show()
