JCC = javac
JSON = ./json-simple-1.1.1.jar
JFLAGS = -g -cp $(JSON)
PY = python2

Prob4.class:	Prob4.java json-simple-1.1.1.jar
	$(JCC) $(JFLAGS) Prob4.java

data/vert-rares.dat: Prob4.class data/vert.counts data/parse_train_vert.dat json-simple-1.1.1.jar
	java -cp .:$(JSON) Prob4 data/vert.counts data/parse_train_vert.dat data/vert-rares.dat

data/vr.counts: data/count_cfg_freq.py data/vert-rares.dat
	$(PY) data/count_cfg_freq.py data/vert-rares.dat > data/vr.counts

data/vert.counts: data/count_cfg_freq.py data/parse_train_vert.dat
	$(PY) data/count_cfg_freq.py data/parse_train_vert.dat > data/vert.counts

data/cfg.counts: data/count_cfg_freq.py data/parse_train.dat
	$(PY) data/count_cfg_freq.py data/parse_train.dat > data/cfg.counts

data/rare.counts: data/count_cfg_freq.py data/rares.dat
	$(PY) data/count_cfg_freq.py data/rares.dat > data/rare.counts

data/rares.dat: Prob4.class json-simple-1.1.1.jar data/cfg.counts data/parse_train.dat
	java -cp .:$(JSON) Prob4 data/cfg.counts data/parse_train.dat data/rares.dat

data/cky.results: prob5.py data/rare.counts data/parse_dev.dat
	$(PY) prob5.py data/rare.counts data/parse_dev.dat > data/cky.results

data/vr.results: prob5.py data/vr.counts data/parse_dev.dat
	$(PY) prob5.py data/vr.counts data/parse_dev.dat > data/vr.results

.PHONY: clean
clean:
	rm -f *.class data/*.counts data/*.results data/*rare*

.PHONY: eval
eval: data/eval_parser.py data/parse_dev.key data/cky.results
	$(PY) data/eval_parser.py data/parse_dev.key data/cky.results

.PHONY: vEval
vEval: data/eval_parser.py data/parse_dev.key data/vr.results
	$(PY) data/eval_parser.py data/parse_dev.key data/vr.results