import pipe_servers as p
from sys import argv
import time
import re

def isCap(word):
	return "true" if ord(word[0]) >= 65 and ord(word[0]) <= 90 else "false"

def hasLetters(word):
	for c in word:
		if ord(c) >= 65 and ord(c) <= 90 or ord(c) >= 97 and ord(c) <= 122:
			return "true"
	return "false"

def scoreGen(gen, eg):
	egLines = eg.split("\n")
	scored = ""
	for line in gen.split("\n"):
		hist = re.split("[ \t]+", line)
		if len(hist) != 3:
			continue
		word = re.split("[ \t]+", egLines[int(hist[0])-1])[0]

		#bigram features
		bKey = "BIGRAM:"+hist[1]+":"+hist[2]
		if bKey not in v: v[bKey] = 0 
		gBIGRAM = v[bKey]

		#word/tag features
		
		tKey = "TAG:"+word+":"+hist[2]
		if tKey not in v: v[tKey] = 0 
		gTAG = v[tKey]
		
		#word length/tag features
		lKey = "LEN:"+str(len(word))+":"+hist[2]
		if lKey not in v: v[lKey] = 0
		gLEN = v[lKey]
		
		#capitalized/tag features
		cKey = "CAP:"+isCap(word)+":"+hist[2]
		if cKey not in v: v[cKey] = 0
		gCAP = v[cKey]

		#has letters / tag features
		hKey = "LET:"+hasLetters(word)+":"+hist[2]
		if hKey not in v: v[hKey] = 0
		gLET = v[hKey]

		scored += line + " %s\n" % str(gBIGRAM + gTAG + gLEN)

	return scored

def updateV(y, z, eg):
	global v, v
	egLines = eg.split("\n")
 	yLines = y.split("\n")
 	zLines = z.split("\n")

 	#assemble feature vectors for y and z
 	for i in range(min(len(yLines)-1, len(zLines)-1)):
 		yLine = re.split("[ \t]+", yLines[i])
 		zLine = re.split("[ \t]+", zLines[i])
 		word = re.split("[ \t]+", egLines[int(yLine[0])-1])[0]
 		
 		#update bigram tag parameters
 		v["BIGRAM:"+yLine[1]+":"+yLine[2]] += 1
 		v["BIGRAM:"+zLine[1]+":"+zLine[2]] -= 1
 		
 		#update word/tag parameters
		v["TAG:"+word+":"+yLine[2]] += 1
		v["TAG:"+word+":"+zLine[2]] -= 1
		"""
		#update word length / tag parameters
		v["LEN:"+str(len(word))+":"+yLine[2]] += 1
		v["LEN:"+str(len(word))+":"+zLine[2]] -= 1
		
		#update capitalized / tag parameters
		v["CAP:"+isCap(word)+":"+yLine[2]] += 1
		v["CAP:"+isCap(word)+":"+zLine[2]] -= 1
		"""
		#update has letters / tag parameters
		v["LET:"+hasLetters(word)+":"+yLine[2]] += 1
		v["LET:"+hasLetters(word)+":"+zLine[2]] -= 1
		
if __name__ == "__main__":
	if len(argv) != 5:
		print "usage: python %s <training_data> <history_generator> <dev_data> <decoder>"
		exit(1)

	v = dict()

	#perceptron training
	examples = open(argv[1]).read().split("\n\n")
	iterations = 5
	for i in range(iterations):
		goldProc = p.process(["python", argv[2], "GOLD"])
		enumProc = p.process(["python", argv[2], "ENUM"])
		decProc = p.process(["python", argv[4], "HISTORY"])

		for eg in examples:
			y = p.call(goldProc, eg)
			gen = p.call(enumProc, eg)
			scored = scoreGen(gen, eg)
			z = p.call(decProc, scored.rstrip())
			updateV(y, z, eg)

		goldProc.kill()
		enumProc.kill()
		decProc.kill()
	
	for f in v.keys():
		print "%s %s" % (f, v[f])