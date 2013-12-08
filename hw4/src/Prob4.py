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

def scoreHist(hist, sent, v):
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
		scored += line + "%5s\n" % str(gBIGRAM + gTAG)
	return scored

if __name__ == "__main__":
	if(len(argv) != 5):
		print "usage: python %s <parameters_file> <history_generator> <dev_data> <decoder>" % argv[0]
		exit(1)

	v = getV(argv[1])
	sentences = open(argv[3]).read().split("\n\n")
	histProc = p.process(["python", argv[2], "ENUM"])
	
	
	for s in sentences:
		hist = p.call(histProc, s)
		scored = scoreHist(hist, s, v)
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