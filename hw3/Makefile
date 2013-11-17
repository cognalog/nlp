JAVA = javac

Prob4.class: Prob4.java EMRecord.java EMParam1.java
	$(JAVA) Prob4.java

Prob5.class: Prob5.java Prob4.class EM2Result.java
	$(JAVA) Prob5.java

PHONY: clean
clean:
	rm *.class

PHONY: run4.1
run4.1: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt top10

PHONY: run4.2
run4.2: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt align

PHONY: time4
time4: Prob4.class data/corpus.en data/corpus.de data/devwords.txt
	java Prob4 data/corpus.en data/corpus.de data/devwords.txt time

PHONY: run5
run5: Prob5.class data/corpus.en data/corpus.de
	java Prob5 data/corpus.en data/corpus.de