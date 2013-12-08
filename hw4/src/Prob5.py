import pipe_servers as p
import re
import time
from sys import argv

def scoreGen(gen, eg, v):
	egLines = eg.split("\n")
	scored = ""
	for line in gen.split("\n"):
		hist = re.split("[ \t]+", line)
		if len(hist) != 3:
			continue
		bKey = "BIGRAM:"+hist[1]+":"+hist[2]
		if bKey not in v: v[bKey] = 0 
		gBIGRAM = v[bKey]

		word = re.split("[ \t]+", egLines[int(hist[0])-1])[0]
		tKey = "TAG:"+word+":"+hist[2]
		if tKey not in v: v[tKey] = 0 
		gTAG = v[tKey]

		suf1 = word[len(word)-1:]
		s1Key = "SUFF:"+suf1+":"+hist[2]
		if s1Key not in v: v[s1Key] = 0 
		gSUFF1 = v[s1Key]
		gSUFF2 = 0
		gSUFF3 = 0
		if len(word) >= 2:
			suf2 = word[len(word)-2:]
			s2Key = "SUFF:"+suf2+":"+hist[2]
			if s2Key not in v: v[s2Key] = 0 
			gSUFF2 = v[s2Key]

			if len(word) >= 3:
				suf3 = word[len(word)-3:]
				s3Key = "SUFF:"+suf3+":"+hist[2]
				if s3Key not in v: v[s3Key] = 0 
				gSUFF3 = v[s3Key]

		scored += line + "%5s\n" % str(gBIGRAM + gTAG + gSUFF1 + gSUFF2 + gSUFF3)

	return scored

def updateV(y, z, eg, v):
	egLines = eg.split("\n")
 	yLines = y.split("\n")
 	zLines = z.split("\n")
 	yFV = dict()
 	zFV = dict()
 	#assemble feature vectors for y and z
 	for i in range(min(len(yLines)-1, len(zLines)-1)):
 		yLine = re.split("[ \t]+", yLines[i])
 		zLine = re.split("[ \t]+", zLines[i])

 		bY = "BIGRAM:"+yLine[1]+":"+yLine[2]
 		yFV[bY] = 1 if bY not in yFV else yFV[bY] + 1
 		bZ = "BIGRAM:"+zLine[1]+":"+zLine[2]
 		zFV[bZ] = 1 if bZ not in zFV else zFV[bZ] + 1

 		word = re.split("[ \t]+", egLines[int(yLine[0])-1])[0]
		tY = "TAG:"+word+":"+yLine[2]
		yFV[tY] = 1 if tY not in yFV else yFV[tY] + 1
		tZ = "TAG:"+word+":"+zLine[2]
		zFV[tZ] = 1 if tZ not in zFV else zFV[tZ] + 1

		suf1 = word[len(word)-1:]
		s1Y = "SUFF:"+suf1+":"+yLine[2]
		yFV[s1Y] = 1 if s1Y not in yFV else yFV[s1Y] + 1
		s1Z = "SUFF:"+suf1+":"+zLine[2]
		zFV[s1Z] = 1 if s1Z not in zFV else zFV[s1Z] + 1

		if len(word) < 2:
			continue
		suf2 = word[len(word)-2:]
		s2Y = "SUFF:"+suf2+":"+yLine[2]
		yFV[s2Y] = 1 if s2Y not in yFV else yFV[s2Y] + 1
		s2Z = "SUFF:"+suf2+":"+zLine[2]
		zFV[s2Z] = 1 if s2Z not in zFV else zFV[s2Z] + 1

		if len(word) < 3:
			continue
		suf3 = word[len(word)-3:]
		s3Y = "SUFF:"+suf3+":"+yLine[2]
		yFV[s3Y] = 1 if s3Y not in yFV else yFV[s3Y] + 1
		s3Z = "SUFF:"+suf3+":"+zLine[2]
		zFV[s3Z] = 1 if s3Z not in zFV else zFV[s3Z] + 1
	#add the feature vector difference to v
	for f in yFV.keys():
		v[f] += yFV[f]
	for f in zFV.keys():
		v[f] -= zFV[f]

if __name__ == "__main__":
	if len(argv) != 5:
		print "usage: python %s <training_data> <history_generator> <dev_data> <decoder>"
		exit(1)

	t = time.clock()
	v = dict()
	#perceptron training
	examples = open(argv[1]).read().split("\n\n")
	iterations = 1
	for i in range(iterations):
		goldProc = p.process(["python", argv[2], "GOLD"])
		enumProc = p.process(["python", argv[2], "ENUM"])
		for eg in examples:
			y = p.call(goldProc, eg)
			gen = p.call(enumProc, eg)
			scored = scoreGen(gen, eg, v)
			decProc = p.process(["python", argv[4], "HISTORY"])
			z = p.call(decProc, scored)
			updateV(y, z, eg, v)
		goldProc.kill()
		enumProc.kill()
	
	for f in v.keys():
		print "%s %s" % (f, v[f])