JAVA = javac

Prob4.class: Prob4.java EMRecord.java EMParam1.java
	$(JAVA) Prob4.java

data/dev.matches: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt top10 > data/dev.matches

data/ibm1.aligns: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt align > data/ibm1.aligns

Prob5.class: Prob5.java Prob4.class EM2Result.java
	$(JAVA) Prob5.java

data/ibm2.aligns: Prob5.class data/corpus.en data/corpus.de
	java Prob5 data/corpus.en data/corpus.de > data/ibm2.aligns

Prob6.class: Prob6.java Prob5.class
	$(JAVA) Prob6.java

data/unscrambled.en: Prob6.class data/corpus.en data/corpus.de data/scrambled.en data/original.de
	java Prob6 data/corpus.en data/corpus.de data/scrambled.en data/original.de > data/unscrambled.en

PHONY: clean
clean:
	rm *.class data/*.matches data/*.aligns

PHONY: time4
time4: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt time

PHONY: run6
run6: Prob6.class data/corpus.en data/corpus.de data/scrambled.en data/original.de
	java Prob6 data/corpus.en data/corpus.de data/scrambled.en data/original.de

PHONY: eval
eval: data/eval_scramble.py data/unscrambled.en data/original.en
	python data/eval_scramble.py data/unscrambled.en data/original.en