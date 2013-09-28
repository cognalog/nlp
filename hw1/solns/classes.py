from rares import getRares
import sys

#returns whether a word has no alphabetic characters
def noAlpha(word):
	if word == "":
		return True
	i = ord(word[0])
	if (i < 65 or i > 90) and (i < 97 or i > 122):
		return noAlpha(word[1:])
	else:
		return False

def abbrev(word):
	if word == "":
		return True
	i = ord(word[0])
	if i > 64 and i < 91 or word[0] == '.':
		return abbrev(word[1:])
	else:
		return False

#return the classification (based on lexical properties) for a word
def classify(word):
	if 'land' in word:
		return '_probLoc_'
	if abbrev(word):
		return '_abbrev_'
	if word == word.capitalize() and word != word.upper():
		return '_firstCapOnly_'
	if word == word.capitalize():
		return '_firstOrAllCaps_'
	if word == word.lower() or noAlpha(word):
		return '_probO_'
	return '_weirdo_'

"""
creates a new training file, where each word below the frequency threshold=5 is
replaced by the class name _RARE_
"""
def classiFile(oldF, newF):
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
			temp[0] = classify(temp[0])
		newTrain.write(" ".join(temp) + "\n")
	newTrain.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: python "+sys.argv[0]+" <training_file> <new_training_file>"
	else:
		classiFile(sys.argv[1], sys.argv[2])