import java.util.ArrayList;
import java.util.HashMap;
import java.io.*;

public class Prob4{
	static String eFName;
	static String fFName;
	static PrintStream stdout = System.out;

	/*
	* gives an initial value for t(f | e) for a particular e regardless of f
	*/
	private static HashMap<String, HashMap<String, Double>> initialTs() throws IOException{
		BufferedReader engFile = new BufferedReader(new FileReader(eFName));
		BufferedReader forFile = new BufferedReader(new FileReader(fFName));
		ArrayList<Integer> lines = new ArrayList();
		HashMap<String, HashMap<String, Double>> emissions = new HashMap();
		
		String eline, fline;
		//find which english corpus lines contain the word
		while((eline = engFile.readLine()) != null){
			fline = forFile.readLine();
			for(String e : eline.split(" ")){
				if(!emissions.containsKey(e))
					emissions.put(e, new HashMap());
				for(String f : fline.split(" ")){
					emissions.get(e).put(f, -1.0);
				}
			}
		}
		return emissions;
	}
	/*
	public static HashMap<String, HashMap<String, Double>> emAlg(int iterations) throws IOException{
		HashMap<String, HashMap<String, Double>> params = initialTs();
		for(int its = 0; its < iterations; its++){//for s = 1..S
			BufferedReader engFile = new BufferedReader(new FileReader(eFName));
			BufferedReader forFile = new BufferedReader(new FileReader(fFName));
			String eline, fline;
			while((eline = engFile.readLine()) != null){//for k = 1..n
				fline = forFile.readLine();
				int i = 0; //foreign word index
				for(String f : fline.split(" ")){//for i = 1..mk
					int j = 0; //english word index
					for(String e : eline.split(" ")){//for j = 0..lk

						j++;
					}
					i++;
				}
			}
		}
		
		return params;
	}
*/
	public static void main(String[] args) throws IOException{
		if(args.length < 2){
			stdout.println("usage: java Prob4 <english_corpus> <german_corpus>");
			return;
		}
		//make readers for english and german corpora
		eFName = args[0];
		fFName = args[1];
		System.out.println(1.0 / initialTs().get("resumption").size());
	}
}