import pipe_servers as p
import re
from sys import argv

def getV(file):
	v = dict()
	vFile = open(file).read()
	for param in vFile.split("\n"):
		line = param.split(" ")
		if len(line) == 2:
			v[line[0]] = float(line[1])
	return v

def scoreHist(hist, sent, v, suff):
	words = sent.split("\n")
	scored = ""
	for line in hist.split("\n"):
		parts = re.split(" +", line)
		if len(parts) < 3:
			continue
		bKey = "BIGRAM:"+parts[1]+":"+parts[2]
		gBIGRAM = v[bKey] if bKey in v else 0

		tKey = "TAG:"+words[int(parts[0])-1]+":"+parts[2]
		gTAG = v[tKey] if tKey in v else 0

		gSUFF1 = 0
		gSUFF2 = 0
		gSUFF3 = 0
		if(suff == "y"):
			word = words[int(parts[0])-1]
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

if __name__ == "__main__":
	if(len(argv) != 6):
		print "usage: python %s <parameters_file> <history_generator> <dev_data> <decoder> <include_suffixes? (y/n)>" % argv[0]
		exit(1)

	v = getV(argv[1])
	sentences = open(argv[3]).read().split("\n\n")
	histProc = p.process(["python", argv[2], "ENUM"])
	
	
	for s in sentences:
		hist = p.call(histProc, s)
		scored = scoreHist(hist, s, v, argv[5])
		decProc = p.process(["python", argv[4], "HISTORY"])
		histMax = p.call(decProc, scored)
		#decProc dies after this

		#time to format the arg max for evaluation...thanks for the busy work!
		words = s.split("\n")
		hLines = histMax.split("\n")
		for line in hLines:
			parts = re.split(" +", line)
			if len(parts) == 3 and parts[2] != "STOP":
				print "%s %5s" % (words[int(parts[0])-1], parts[2])
		print #I wasted 10 minutes wondering why I was getting .187...then I added this.