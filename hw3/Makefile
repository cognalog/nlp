JAVA = javac

Prob4.class: Prob4.java
	$(JAVA) Prob4.java

PHONY: clean
clean:
	rm *.class

PHONY: run4
run4: Prob4.class data/corpus.en data/corpus.de
	java Prob4 data/corpus.en data/corpus.de