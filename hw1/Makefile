PY = python

data/ner.counts: data/count_freqs.py data/ner_train.dat
	$(PY) data/count_freqs.py data/ner_train.dat > data/ner.counts

data/rare_train.dat: solns/rares.py data/ner_train.dat
	$(PY) solns/rares.py data/ner_train.dat > data/rare_train.dat

data/rare.counts: data/count_freqs.py data/rare_train.dat
	$(PY) data/count_freqs.py data/rare_train.dat > data/rare.counts

data/hmm.results: solns/hmm.py data/rare.counts data/ner_dev.dat
	$(PY) solns/hmm.py data/rare.counts data/ner_dev.dat > data/hmm.results

data/vit.results: solns/viterbi.py data/rare.counts data/ner_dev.dat
	$(PY) solns/viterbi.py data/rare.counts data/ner_dev.dat > data/vit.results

.PHONY: clean
clean:
	rm data/*.counts data/*rare* data/*.results

.PHONY: eval4
eval4: data/eval_ne_tagger.py data/ner_dev.key data/hmm.results
	$(PY) data/eval_ne_tagger.py data/ner_dev.key data/hmm.results 

.PHONY: eval5
eval5: data/eval_ne_tagger.py data/ner_dev.key data/vit.results
	$(PY) data/eval_ne_tagger.py data/ner_dev.key data/vit.results