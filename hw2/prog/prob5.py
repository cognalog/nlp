from sys import argv
from math import log

#returns (rule list, rule counts)
def getRuleCounts(fname):
	cf = open(fname)
	cfStr = cf.read()
	counts = dict()
	rules = dict()
	for line in cfStr.split("\n"):
		lArr = line.split(" ")
		if len(lArr) == 3:
			counts[lArr[2]] = (lArr[0], dict())
		elif len(lArr) == 4:
			counts[lArr[2]][1][lArr[3]] = (lArr[0], dict())
		elif len(lArr) == 5:
			if lArr[2] not in rules:
				rules[lArr[2]] = []
			rules[lArr[2]].append((lArr[3], lArr[4]))
			if lArr[3] in counts[lArr[2]][1]:
				counts[lArr[2]][1][lArr[3]][1][lArr[4]] = lArr[0]
			else:
				counts[lArr[2]][1][lArr[3]] = (0, dict())
				counts[lArr[2]][1][lArr[3]][1][lArr[4]] = lArr[0]
	cf.close()
	return (rules, counts)

#gets a nonterminal or binary/unary rule count using the dynamic table
def getCount(table, *args):
	if len(args) < 1:
		return 0
	if args[0] in table:
		if len(args) == 1:
			return table[args[0]][0]
		elif args[1] in table[args[0]][1]:
			if len(args) == 2:
				return table[args[0]][1][args[1]][0]
			elif args[2] in table[args[0]][1][args[1]][1]:
				if len(args) == 3:
					return table[args[0]][1][args[1]][1][args[2]]
	return 0

#function for maximum likelihood estimate
def getQ(table, *args):
	if len(args) == 2 and args[0] in table:
		return float(getCount(table, args[0], args[1])) / float(getCount(table, args[0]))
	elif len(args) == 3 and args[0] in table:
		return float(getCount(table, args[0], args[1], args[2])) / float(getCount(table, args[0]))
	else:
		return 0

def stored(table, i, j, x):
	return i in table and j in table[i] and x in table[i][j]

def pi(table, pt, rules, words, i, j, x):
	#print("%s %d-%d" % (x,i,j))
	if(i == j):
		return ([x, words[i-1]], getQ(table, x, words[i-1]))
	aMax = [x, '~', '~']
	pMax = 0
	if x in rules:
		for (y, z) in rules[x]:
			for s in range(i, j):
				#skip the recursion if the pi value's been stored
				if stored(pt, i, s, y):
					py = pt[i][s][y]
				else:
					py = pi(table, pt, rules, words, i, s, y)
				if stored(pt, s+1, j, z):
					pz = pt[s+1][j][z]
				else:
					pz = pi(table, pt, rules, words, s+1, j, z)
				q = getQ(table, x, y, z)
				if py[1] > 0 and pz[1] > 0 and q > 0:
					p = abs(log(q, 2) + log(py[1], 2) + log(pz[1], 2))
				else:
					p = 0
				if p > pMax:
					aMax[1] = py[0] #update arg max
					aMax[2] = pz[0]
					pMax = p #update max
	#store this pi value for later use
	pt[i][j][x] = (aMax, pMax)
	return (aMax, pMax)
	
if __name__ == "__main__":
	if(len(argv) != 3):
		print("usage: python %s <counts_file> <dev_file>" % argv[0])
	else:
		nfo = getRuleCounts(argv[1])
		rules = nfo[0]
		cTable = nfo[1] #cTable.keys() gives all nonterms
		devF = open(argv[2])
		for line in devF.read().split("\n"):
			words = line.split(" ")
			#set up the table
			piTable = dict()
			for i in range(1,len(words)+1):
				piTable[i] = dict()
				for j in range(i+1,len(words)+1):
					piTable[i][j] = dict()
			pv = pi(cTable, piTable, rules, words, 1, len(words), "S")
			if(pv[1] > 0):
				print(pv[0])
			else: #if we're dealing w/ a sentence fragment
				aMax = []
				pMax = 0
				for x in cTable.keys():
					pv = pi(cTable, piTable, rules, words, 1, len(words), x)
					if(pv[1] > pMax):
						pMax = pv[1]
						aMax = pv[0]
				print(aMax)