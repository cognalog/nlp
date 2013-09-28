import sys
import math
from rares import getRares
from classes import classify
from hmm import storeData
from trigs import storeCounts

#returns the log of the emission parameter given x, y and the event counts
def getEmission(x, y, store):
	if y not in store[x]:
		return 0
	num = store[x][y]
	denom = store[y]
	return math.log(float(num)/float(denom), 2) if num != 0 and denom != 0 else 0

"""
uses count data to find a trigram's transition parameter
returns the log estimate
"""
def getQ (y1, y2, y3, grams):
	if(y1 not in grams):
		return 0
	num = grams[y1].gramCount(y2, y3)
	denom = grams[y1].gramCount(y2)
	return math.log(float(num) / float(denom), 2) if num != 0 and denom != 0 else 0

def pi (k, u, v):
	if wordSeq[k-1] in infreq or wordSeq[k-1] not in emStruct:
		#determines whether _RARE_ or classify is used
		word = "_RARE_"
	else:
		word = wordSeq[k-1]
	maxW = ''
	maxP = 0
	for w in getS(k-2):
		p =  table[k-1][w][u][1] + getQ(w, u, v, tranStruct) * getEmission(word, v, emStruct)
		if p > maxP:
			maxP = p
			maxW = w
	table[k][u][v] = (maxW, maxP)
	#for testing purposes
	#return (maxW, maxP)


def getS(k):
	if k < 1:
		return ['*']
	elif wordSeq[k-1] in infreq or wordSeq[k-1] not in emStruct:
		#another choice point for_RARE_ or classify
		return emStruct["_RARE_"]
	else:
		return emStruct[wordSeq[k-1]]

#extract data from counts file
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "usage: "+sys.argv[0]+" <counts_file> <test_file>"
	else:
		cFile = open(sys.argv[1])
		tFile = open(sys.argv[2])
		cData = cFile.read()
		wordSeq = tFile.read().split("\n")
		cFile.close()
		tFile.close()

		#structure data
		tranStruct = storeCounts(sys.argv[1])
		emStruct = storeData(cData)
		infreq = getRares(cData)
		n = len(wordSeq)
		y = dict()
		z = dict()
		table = dict()

		#fill up the dynamic programming table with pi values
		table[0] = {'*': {'*': ('',1)}}
		for k in xrange(1,n+1):
			table[k] = dict()
			for u in getS(k-1):
				table[k][u] = dict()
				for v in getS(k):
					p = pi(k, u, v)
					#print str(k)+' '+u+' '+v+' '+str(p)

		#get u and v with highest pi at n
		maxU = ''
		maxV = ''
		maxP = 0
		for u in getS(n-1):
			for v in getS(n):
				p = table[n][u][v][1] + getQ(u,v,'STOP',tranStruct)
				if p > maxP:
					maxP = p
					maxV = v
					maxU = u
		y[n] = maxV
		y[n-1] = maxU
		z[n] = z[n-1] = maxP

		#work backward from the last two tags to get the whole sequence
		for k in reversed(xrange(1, n-1)):
			y[k] = table[k+2][y[k+1]][y[k+2]][0]
			z[k] = table[k+2][y[k+1]][y[k+2]][1]

		for i in y:
			if(len(wordSeq[i-1]) < 1):
				print ""
				continue
			print wordSeq[i-1] + " " + y[i] + " " + str(z[i])