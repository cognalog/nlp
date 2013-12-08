data/prob4.out: src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
		python src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py > data/prob4.out

data/suffix_tagger.model: src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py > data/suffix_tagger.model

.PHONY: clean
clean:
	rm src/*.pyc data/*.pyc data/*.out

.PHONY: eval4
eval4: data/eval_tagger.py data/tag_dev.key data/prob4.out
	python data/eval_tagger.py data/tag_dev.key data/prob4.out

.PHONY: run5
run5: src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py