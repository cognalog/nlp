JCC = javac
JSON = ./json-simple-1.1.1.jar
JFLAGS = -g -cp $(JSON)

Prob4.class:	Prob4.java json-simple-1.1.1.jar
	$(JCC) $(JFLAGS) Prob4.java

data/vert-rares.dat: Prob4.class data/vert.counts data/parse_train_vert.dat json-simple-1.1.1.jar
	java -cp .:$(JSON) Prob4 data/vert.counts data/parse_train_vert.dat data/vert-rares.dat

data/vr.counts: data/count_cfg_freq.py data/vert-rares.dat
	python2 data/count_cfg_freq.py data/vert-rares.dat > data/vr.counts

data/vert.counts: data/count_cfg_freq.py data/parse_train_vert.dat
	python2 data/count_cfg_freq.py data/parse_train_vert.dat > data/vert.counts

data/cfg.counts: data/count_cfg_freq.py data/parse_train.dat
	python2 data/count_cfg_freq.py data/parse_train.dat > data/cfg.counts

data/rare.counts: data/count_cfg_freq.py data/rares.dat
	python2 data/count_cfg_freq.py data/rares.dat > data/rare.counts

data/rares.dat: run4

.PHONY: clean
clean:
	rm -f *.class data/*.counts

.PHONY: run4
run4: Prob4.class json-simple-1.1.1.jar data/cfg.counts data/parse_train.dat
	java -cp .:$(JSON) Prob4 data/cfg.counts data/parse_train.dat data/rares.dat

.PHONY: run5
run5: prob5.py data/rare.counts data/parse_dev.dat
	python2 prob5.py data/rare.counts data/parse_dev.dat > data/cky.results

.PHONY: run6
run6: prob5.py data/vr.counts data/parse_dev.dat
	python2 prob5.py data/vr.counts data/parse_dev.dat > data/cky.results


.PHONY: eval
eval: run5 data/eval_parser.py data/parse_dev.key 
	python2 data/eval_parser.py data/parse_dev.key data/cky.results