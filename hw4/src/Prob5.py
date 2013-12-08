import pipe_servers as p
import re
import time
from sys import argv

def scoreGen(gen, eg):
	global vB, vT, vS1, vS2, vS3
	egLines = eg.split("\n")
	scored = ""
	for line in gen.split("\n"):
		hist = re.split("[ \t]+", line)
		if len(hist) != 3:
			continue
		bKey = "BIGRAM:"+hist[1]+":"+hist[2]
		if bKey not in vB: vB[bKey] = 0 
		gBIGRAM = vB[bKey]

		word = re.split("[ \t]+", egLines[int(hist[0])-1])[0]
		tKey = "TAG:"+word+":"+hist[2]
		if tKey not in vT: vT[tKey] = 0 
		gTAG = vT[tKey]

		suf1 = word[len(word)-1:]
		s1Key = "SUFF:"+suf1+":"+hist[2]
		if s1Key not in vS1: vS1[s1Key] = 0 
		gSUFF1 = vS1[s1Key]
		gSUFF2 = 0
		gSUFF3 = 0
		if len(word) >= 2:
			suf2 = word[len(word)-2:]
			s2Key = "SUFF:"+suf2+":"+hist[2]
			if s2Key not in vS2: vS2[s2Key] = 0 
			gSUFF2 = vS2[s2Key]

			if len(word) >= 3:
				suf3 = word[len(word)-3:]
				s3Key = "SUFF:"+suf3+":"+hist[2]
				if s3Key not in vS3: vS3[s3Key] = 0 
				gSUFF3 = vS3[s3Key]

		scored += line + " %s\n" % str(gBIGRAM + gTAG + gSUFF1 + gSUFF2 + gSUFF3)

	return scored

def updateV(y, z, eg):
	global vB, vT, vS1, vS2, vS3
	egLines = eg.split("\n")
 	yLines = y.split("\n")
 	zLines = z.split("\n")

 	#assemble feature vectors for y and z
 	for i in range(min(len(yLines)-1, len(zLines)-1)):
 		yLine = re.split("[ \t]+", yLines[i])
 		zLine = re.split("[ \t]+", zLines[i])

 		vB["BIGRAM:"+yLine[1]+":"+yLine[2]] += 1
 		vB["BIGRAM:"+zLine[1]+":"+zLine[2]] -= 1

 		word = re.split("[ \t]+", egLines[int(yLine[0])-1])[0]
		vT["TAG:"+word+":"+yLine[2]] += 1
		vT["TAG:"+word+":"+zLine[2]] -= 1

		suf1 = word[len(word)-1:]
		vS1["SUFF:"+suf1+":"+yLine[2]] += 1
		vS1["SUFF:"+suf1+":"+zLine[2]] -= 1

		if len(word) < 2:
			continue
		suf2 = word[len(word)-2:]
		vS2["SUFF:"+suf2+":"+yLine[2]] += 1
		vS2["SUFF:"+suf2+":"+zLine[2]] -= 1

		if len(word) < 3:
			continue
		suf3 = word[len(word)-3:]
		vS3["SUFF:"+suf3+":"+yLine[2]] += 1
		vS3["SUFF:"+suf3+":"+zLine[2]] -= 1

if __name__ == "__main__":
	if len(argv) != 5:
		print "usage: python %s <training_data> <history_generator> <dev_data> <decoder>"
		exit(1)

	vB = dict()
	vT = dict()
	vS1 = dict()
	vS2 = dict()
	vS3 = dict()

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
	for f in vB.keys():
		print "%s %s" % (f, vB[f])
	for f in vT.keys():
		print "%s %s" % (f, vT[f])
	for f in vS1.keys():
		print "%s %s" % (f, vS1[f])
	for f in vS2.keys():
		print "%s %s" % (f, vS2[f])
	for f in vS3.keys():
		print "%s %s" % (f, vS3[f])