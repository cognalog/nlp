JAVA = javac

Prob4.class: Prob4.java EMRecord.java EMParam1.java
	$(JAVA) Prob4.java

Prob5.class: Prob5.java
	$(JAVA) Prob5.java

data/ibm1.params: Prob4.class
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt serve > data/ibm1.params

PHONY: clean
clean:
	rm *.class data/*.params

PHONY: run4.1
run4.1: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt top10

PHONY: run4.2
run4.2: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt align

#add ibm1.params to dependencies
PHONY: run5
run5: Prob5.class data/corpus.en data/corpus.de
	java Prob5 data/corpus.en data/corpus.de data/ibm1.params