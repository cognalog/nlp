import org.json.simple.*;
import org.json.simple.parser.*;
import java.io.*;
import java.util.HashMap;

public class Prob4{
	
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
		if(args.length < 3){
			System.out.println("usage: java Prob4 <counts_file> <training_file> <replacement_file>");
			return;
		}
		try{
			FileReader countFR = new FileReader(args[0]);
			FileReader trainFR = new FileReader(args[1]);
			FileWriter repFW = new FileWriter(args[2]);
			BufferedReader countBR = new BufferedReader(countFR);
			BufferedReader trainBR = new BufferedReader(trainFR);
			BufferedWriter repBW = new BufferedWriter(repFW, 1);
			String line = null;

			//get counts for each word among all the trees
			HashMap<String, Integer> counts = new HashMap<String, Integer>();
			while((line = countBR.readLine()) != null){
				String[] parts = line.split(" ");
				if(parts[1].equals("UNARYRULE")){
					String word = parts[3];
					if(counts.containsKey(word))
						counts.put(word, counts.get(word) + Integer.parseInt(parts[0]));
					else
						counts.put(word, Integer.parseInt(parts[0]));
				}
			}
			countFR.close();

			//find rare words within counts
			HashMap<String, Integer> rares = new HashMap<String, Integer>();
			for(String word : counts.keySet()){
				if(counts.get(word) < 5)
					rares.put(word, counts.get(word));
			}

			JSONParser parser = new JSONParser();
			while((line = trainBR.readLine()) != null){
				JSONArray tree = (JSONArray)parser.parse(line);
				repBW.write(replaceRares(tree, rares).toString()+"\n");
			}
			trainFR.close();
			repFW.close();
			System.out.println(line);


			trainFR.close();

		}catch(Exception e){
			System.out.println(e);
		}
	}
}