import org.json.simple.*;
import org.json.simple.parser.*;
import java.io.*;
import java.util.HashMap;

public class Prob4{
	//records the counts for the terminal words in the tree in a given HashMap. Mutates the external HashMap
	public static void getWordCounts(JSONArray tree, HashMap<String, Integer> counts){
		if(tree.size() == 2){ //rule is unary
			String word = (String)tree.get(1);
			if(counts.containsKey(word))
				counts.put(word, counts.get(word)+1);
			else
				counts.put(word, 1);
		}else{ //rule is binary
			getWordCounts((JSONArray)tree.get(1), counts);
			getWordCounts((JSONArray)tree.get(2), counts);
		}
	}

	public static JSONArray replaceRares(JSONArray tree, HashMap<String, Integer> rares){
		if(tree.size() == 2){
			if(rares.containsKey(tree.get(1)))
				tree.set(1, "_RARE_");
		}else{
			tree.set(1, replaceRares((JSONArray)tree.get(1), rares));
			tree.set(2, replaceRares((JSONArray)tree.get(2), rares));
		}
		return tree;
	}

	public static void main(String[] args){
		if(args.length < 1){
			System.out.println("usage: java Prob4 <training_file>");
			return;
		}
		try{
			FileReader trainFR = new FileReader(args[0]);
			BufferedReader trainBR = new BufferedReader(trainFR);
			String line = null;
			JSONParser parser = new JSONParser();

			//get counts for each word among all the trees
			HashMap<String, Integer> counts = new HashMap<String, Integer>();
			while((line = trainBR.readLine()) != null){
				JSONArray tree = (JSONArray)parser.parse(line);
				getWordCounts(tree, counts);
			}

			//find rare words within counts
			HashMap<String, Integer> rares = new HashMap<String, Integer>();
			for(String word : counts.keySet()){
				if(counts.get(word) < 5)
					rares.put(word, 0);
			}
			System.out.println(rares);

			trainFR.close();
		}catch(Exception e){
			System.out.println(e);
		}
	}
}