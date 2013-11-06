PY = python

data/ner.counts: data/count_freqs.py data/ner_train.dat
	python data/count_freqs.py data/ner_train.dat > data/ner.counts

data/rare_train.dat: solns/rares.py data/ner_train.dat
	python solns/rares.py data/ner_train.dat > data/rare_train.dat

data/rare.counts: data/count_freqs.py data/rare_train.dat

.PHONY: clean
clean:
	rm data/*.counts data/*rare*