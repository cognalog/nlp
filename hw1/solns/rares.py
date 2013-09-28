import sys

#returns a list of infrequent (count < 5) words
def getRares(body):
	counts = dict()
	lines = body.split("\n")
	#get 1-gram word counts from file
	for l in lines:
		if(len(l) == 0):
			continue
		word = l[:l.index(" ")]
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	#replace infrequent words with _RARE_
	infreq = dict()
	for w in counts:
		if counts[w] < 5:
			infreq[w] = 0
	return infreq

"""
creates a file new_train.dat, where each word below the frequency threshold=5 is
replaced by the class name _RARE_
"""
def replaceRares():
	#find the rare words
	oldTrain = open(argv[1])
	oldDat = oldTrain.read()
	oldTrain.close()
	rares = getRares(oldDat)
	#replace the rare words
	newTrain = open(argv[2], 'w')
	for line in oldDat.split("\n"):
		temp = line.split(" ")
		if temp[0] in rares:
			temp[0] = "_RARE_"
		newTrain.write(" ".join(temp) + "\n")
	newTrain.close()

if len(sys.argv) < 3:
	print "usage: python "+argv[0]+" <training_file> <new_training_file>"
elif __name__ == "__main__":
	replaceRares()