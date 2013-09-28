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
creates a new training file, where each word below the frequency threshold=5 is
replaced by the class name _RARE_
"""
def replaceRares(oldF, newF):
	#find the rare words
	oldTrain = open(oldF)
	oldDat = oldTrain.read()
	oldTrain.close()
	rares = getRares(oldDat)
	#replace the rare words
	newTrain = open(newF, 'w')
	for line in oldDat.split("\n"):
		temp = line.split(" ")
		if temp[0] in rares:
			temp[0] = "_RARE_"
		newTrain.write(" ".join(temp) + "\n")
	newTrain.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: python "+sys.argv[0]+" <training_file> <new_training_file>"
	else:
		replaceRares(sys.argv[1], sys.argv[2])