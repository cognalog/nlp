from sys import argv
import re

if __name__ == "__main__":
	if len(argv) != 3:
		print "usage: python %s <output_file> <key_file>" % argv[0]

	out1 = open(argv[1]).read().split("\n")
	out2 = open(argv[2]).read().split("\n")

	for i in range(min(len(out1), len(out2))):
		pair1 = re.split("[ \t]+", out1[i])
		pair2 = re.split("[ \t]+", out2[i])

		if len(pair1) != 2 or len(pair2) != 2:
			continue
		if(pair1[1] != pair2[1]):
			print "Difference: %s:%s, %s:%s" % (pair1[0], pair1[1], pair2[0], pair2[1])