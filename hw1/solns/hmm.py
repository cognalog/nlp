import math
import sys
from classes import classify

#returns the emission parameter given x, y and the event counts
def getEmission(x, y, store):
	if y not in store[x]:
		return 0
	num = store[x][y]
	denom = store[y]
	return float(num)/float(denom)



"""
builds a dictionary for quick access of the data
keys are either words or tags:
	dict[word] = nested dictionary with tags for keys and count(word | tag) for values
	dict[tag] = count(tag)
returns said dictionary
"""
def storeData(body):
	store = dict()
	arr = body.split("\n")
	for line in arr:
		lArr = line.split(" ")
		if len(lArr) <= 1:
			continue
		elif lArr[1] == "WORDTAG":
			if lArr[3] not in store:
				store[lArr[3]] = dict()
			store[lArr[3]][lArr[2]] = lArr[0]
		elif lArr[1] == "1-GRAM":
			store[lArr[2]] = lArr[0]
	return store

#finds the arg(y) max emission parameter
def argMaxEmission(x, struct):
	maxE = 0
	maxY = ""
	if x not in struct:
		#choice point for _RARE_ vs classify
		x = "_RARE_"
	for y in struct[x]:
		em = getEmission(x, y, struct)
		if maxE < em:
			maxE = em
			maxY = y
	return (maxY, maxE)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "usage: python "+sys.argv[0]+" <counts_file> <test_file>"
	else:
		#get emission params from data
		countsF = open(sys.argv[1])
		testF = open(sys.argv[2])
		eventD = countsF.read()
		testD = testF.read()
		countsF.close()
		testF.close()
		struct = storeData(eventD)
		for word in testD.split("\n"):
			if(len(word) < 1):
				print ""
				continue
			ame = argMaxEmission(word, struct)
			print word + " " + ame[0] + " " + str(math.log(ame[1],2))