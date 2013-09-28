import sys
import math
from hmm import storeData
from trigs import storeCounts


def getEmission(x, y, store):
	if x not in store:
		x = "_RARE_"
	if y not in store[x]:
		return 0
	num = store[x][y]
	denom = store[y]
	return -1 * math.log(float(num)/float(denom), 2) if num != 0 and denom != 0 else 0

def getQ (y1, y2, y3, grams):
	if(y1 not in grams):
		return 0
	num = grams[y1].gramCount(y2, y3)
	denom = grams[y1].gramCount(y2)
	return -1 * math.log(float(num) / float(denom), 2) if num != 0 and denom != 0 else 0

def pi (k, u, v):
	global wordSeq
	global tranStruct
	global emStruct
	global table

	maxW = ''
	maxP = 0
	for w in getS(k-2):
		prev = -1 * math.log(table[k-1][w][u], 2) if table[k-1][w][u] > 0 else 0
		p =  prev + getQ(w, u, v, tranStruct) * getEmission(wordSeq[k-1], v, emStruct)
		if p > maxP:
			maxP = p
			maxW = w
	table[k][u][v] = maxP
	return (maxW, maxP)


def getS(k):
	global wordSeq
	global tranStruct

	if k < 1:
		return ['*']  
	elif wordSeq[k] in emStruct:
		return emStruct[wordSeq[k]]
	else:
		return emStruct['_RARE_']

#extract data from counts file
if len(sys.argv) != 3:
	print "usage: "+sys.argv[0]+" <counts_file> <test_file>"
elif __name__ == "__main__":
	cFile = open(sys.argv[1])
	tFile = open(sys.argv[2])
	cData = cFile.read()
	wordSeq = tFile.read().split("\n")
	cFile.close()
	tFile.close()

	#structure data
	tranStruct = storeCounts(sys.argv[1])
	emStruct = storeData(cData)
	table = dict()
	#fill up the dynamic programming table with pi values
	table[0] = {'*': {'*': 1}}
	for k in xrange(1,5):
		table[k] = dict()
		for u in getS(k-1):
			table[k][u] = dict()
			for v in getS(k):
				p = pi(k, u, v)
				print str(k)+' '+u+' '+v+' '+str(p)