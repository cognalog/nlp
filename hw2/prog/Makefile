JCC = javac
JSON = ./json-simple-1.1.1.jar
JFLAGS = -g -cp $(JSON)

Prob4.class:	Prob4.java CNFTree.java
	$(JCC) $(JFLAGS) Prob4.java

.PHONY: clean
clean:
	rm -f *.class

.PHONY: run
run4:
	java -cp .:$(JSON) Prob4 coll/cfg.counts coll/parse_train.dat coll/rares.dat