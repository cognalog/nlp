data/prob4.out: src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py n > data/prob4.out

data/prob5.out: src/Prob4.py data/suffix_tagger.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob4.py data/suffix_tagger.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py y > data/prob5.out

data/prob6.out:  src/Prob4.py data/custom_tagger.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob4.py data/custom_tagger.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py y > data/prob6.out

data/compared.out: data/compare_outputs.py data/prob5.out data/tag_dev.key
	python data/compare_outputs.py data/prob5.out data/tag_dev.key > data/compared.out

data/suffix_tagger.model: src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py > data/suffix_tagger.model

data/custom_tagger.model: src/Prob6.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob6.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py > data/custom_tagger.model

.PHONY: clean
clean:
	rm src/*.pyc data/*.pyc data/*.out

.PHONY: eval4
eval4: data/eval_tagger.py data/tag_dev.key data/prob4.out
	python data/eval_tagger.py data/tag_dev.key data/prob4.out

.PHONY: eval5
eval5: data/eval_tagger.py data/tag_dev.key data/prob5.out
	python data/eval_tagger.py data/tag_dev.key data/prob5.out

.PHONY: eval6
eval6: data/eval_tagger.py data/tag_dev.key data/prob6.out
	python data/eval_tagger.py data/tag_dev.key data/prob6.out

.PHONY: run4
run4: src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob4.py data/tag.model data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py n

.PHONY: run5
run5: src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob5.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py

.PHONY: run6
run6: src/Prob6.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py
	python src/Prob6.py data/tag_train.dat data/tagger_history_generator.py data/tag_dev.dat data/tagger_decoder.py