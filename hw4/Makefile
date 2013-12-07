data/prob4.out: src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
		python src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py > data/prob4.out

.PHONY: clean
clean:
	rm src/*.pyc data/*.pyc data/*.out

.PHONY: eval4
eval4: data/eval_tagger.py data/tag_dev.key data/prob4.out
	python data/eval_tagger.py data/tag_dev.key data/prob4.out