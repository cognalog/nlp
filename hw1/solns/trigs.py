import sys
import math

class Tag:
	def __init__ (self, tp="", ct=0):
		self.type = tp
		self.count = ct
		self.next = dict()
	"""
	adds an n-gram starting with this tag
	just adds another Tag based on params to the next dictionary
	"""
	def addGram (self, tp, ct):
		self.next[tp] = Tag(tp, ct)
	"""
	finds the n-gram count depending on number of params received
	max n = 3, min = 0 (returning -1 for default tags)
	"""
	def gramCount (self, y2=None, y3=None):
		if y2 is None:
			return self.count
		if self.type == "":
			return 0
		if y2 not in self.next:
			return 0
		else:
			return self.next[y2].gramCount(y3)

"""
reads count data from file into a dictionary of tags
"""
def storeCounts (fileName):
	tags = dict()
	tags["*"] = Tag("*", 2)
	ctF = open(fileName)
	lines = ctF.read().split("\n")
	ctF.close()
	for line in lines:
		if(len(line) <= 1):
			continue
		lArr = line.split(" ")
		if lArr[1] == "1-GRAM":
			tags[lArr[2]] = Tag(lArr[2], lArr[0])
		elif lArr[1] == "2-GRAM":
			tags[lArr[2]].addGram(lArr[3], lArr[0])
		elif lArr[1] == "3-GRAM":
			tags[lArr[2]].next[lArr[3]].addGram(lArr[4], lArr[0])
	return tags

"""
uses count data to find a trigram's transition parameter
returns the estimate
"""
def getQ (y1, y2, y3, grams):
	if(y1 not in grams):
		return 0
	num = grams[y1].gramCount(y2, y3)
	denom = grams[y1].gramCount(y2)
	return float(num) / float(denom) if num != 0 and denom != 0 else 0

if len(sys.argv) != 2  and __name__ == "__main__":
	print "usage: python "+sys.argv[0]+" <counts_file>"
elif __name__ == "__main__":
	grams = storeCounts(sys.argv[1])
	while True:
		lArr = raw_input("enter a trigram: ").split(" ")
		q = getQ(lArr[0], lArr[1], lArr[2], grams)
		print q if q == 0 else math.log(q, 2)