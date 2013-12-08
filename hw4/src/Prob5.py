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

		scored += line + " %s\n" % str(gBIGRAM + gTAG + gSUFF1 + gSUFF2 + gSUFF3)

	return scored

def updateV(y, z, eg, v):
	egLines = eg.split("\n")
 	yLines = y.split("\n")
 	zLines = z.split("\n")

 	#assemble feature vectors for y and z
 	for i in range(min(len(yLines)-1, len(zLines)-1)):
 		yLine = re.split("[ \t]+", yLines[i])
 		zLine = re.split("[ \t]+", zLines[i])

 		v["BIGRAM:"+yLine[1]+":"+yLine[2]] += 1
 		v["BIGRAM:"+zLine[1]+":"+zLine[2]] -= 1

 		word = re.split("[ \t]+", egLines[int(yLine[0])-1])[0]
		v["TAG:"+word+":"+yLine[2]] += 1
		v["TAG:"+word+":"+zLine[2]] -= 1

		suf1 = word[len(word)-1:]
		v["SUFF:"+suf1+":"+yLine[2]] += 1
		v["SUFF:"+suf1+":"+zLine[2]] -= 1

		if len(word) < 2:
			continue
		suf2 = word[len(word)-2:]
		v["SUFF:"+suf2+":"+yLine[2]] += 1
		v["SUFF:"+suf2+":"+zLine[2]] -= 1

		if len(word) < 3:
			continue
		suf3 = word[len(word)-3:]
		v["SUFF:"+suf3+":"+yLine[2]] += 1
		v["SUFF:"+suf3+":"+zLine[2]] -= 1

if __name__ == "__main__":
	if len(argv) != 5:
		print "usage: python %s <training_data> <history_generator> <dev_data> <decoder>"
		exit(1)

	t = time.time()
	v = dict()
	#perceptron training
	examples = open(argv[1]).read().split("\n\n")
	iterations = 5
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

	print time.time() - t