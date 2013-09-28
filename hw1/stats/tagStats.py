import sys

if(len(sys.argv)) != 2:
	print 'usage: '+sys.argv[0]+' <key_file>'
else:
	keyF = open(sys.argv[1])
	keyA = keyF.read().split("\n")
	keyF.close()

	binds = dict()
	for line in keyA:
		b = line.split(" ")
		if len(b) < 2:
			continue
		if b[1] not in binds:
			binds[b[1]] = dict()
		if b[0] in binds[b[1]]:
			binds[b[1]][b[0]] += 1
		else:
			binds[b[1]][b[0]] = 1

	for w in binds['I-MISC']:
		print w
