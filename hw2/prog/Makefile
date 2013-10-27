JCC = javac
JSON = ./json-simple-1.1.1.jar
JFLAGS = -g -cp $(JSON)

Prob4.class:	Prob4.java
	$(JCC) $(JFLAGS) Prob4.java

.PHONY: clean
clean:
	rm -f *.class

.PHONY: setup
setup:
	python data/count_cfg_freq.py data/parse_train.dat > data/cfg.counts

.PHONY: rSetup
rSetup: run4
	python data/count_cfg_freq.py data/rares.dat > data/rare.counts

.PHONY: run4
run4: Prob4.class setup
	java -cp .:$(JSON) Prob4 data/cfg.counts data/parse_train.dat data/rares.dat

.PHONY: run5
run5: prob5.py data/cfg.counts data/parse_dev.dat
	python prob5.py data/rare.counts data/parse_dev.dat data/cky.results