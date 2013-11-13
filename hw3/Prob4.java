import java.util.ArrayList;
import java.util.HashMap;
import java.io.*;

public class Prob4{
	static String eFName;
	static String fFName;
	static String tFName;
	static PrintStream stdout = System.out;

	/*
	* gives an initial value for t(f | e) for a particular e regardless of f
	*/
	private static HashMap<String, EMRecord> initialTs() throws IOException{
		BufferedReader engFile = new BufferedReader(new FileReader(eFName));
		BufferedReader forFile = new BufferedReader(new FileReader(fFName));
		HashMap<String, EMRecord> emissions = new HashMap();
		emissions.put("_NULL_", new EMRecord());
		String eline, fline;

		//fully initialize the emissions structure
		while((eline = engFile.readLine()) != null){
			fline = forFile.readLine();
			for(String e : eline.split(" ")){
				if(!emissions.containsKey(e))
					emissions.put(e, new EMRecord());
				for(String f : fline.split(" ")){
					emissions.get("_NULL_").set(f, new EMParam1("_NULL_"));
					emissions.get(e).set(f, new EMParam1(f));
				}
			}
		}
		//now set t params correctly
		emissions.get("_NULL_").setTs();
		for(String e : emissions.keySet()){
			emissions.get(e).setTs();
		}
		return emissions;
	}
	
	public static HashMap<String, EMRecord> emAlg(int iterations) throws IOException{
		HashMap<String, EMRecord> params = initialTs();

		for(int its = 1; its <= iterations; its++){//for s = 1..S
			stdout.println("Starting iteration "+its);
			BufferedReader engFile = new BufferedReader(new FileReader(eFName));
			BufferedReader forFile = new BufferedReader(new FileReader(fFName));
			String eline, fline;
			int k = 1;
			while((eline = engFile.readLine()) != null){//for k = 1..n
				fline = forFile.readLine();
				if(k % 2000 == 0)
					stdout.println("On line "+k);
				int i = 0; //foreign word index
				for(String f : fline.split(" ")){//for i = 1..mk
					int j = 0; //english word index
					double denom = 0;
					for(String e : eline.split(" ")){
						denom += params.get(e).getT(f);
					}
					for(String e : eline.split(" ")){//for j = 0..lk
						double delta = (denom > 0) ? params.get(e).getT(f) / denom : 0;
						params.get(e).increment(f, delta);
						params.get(e).updateT(f, (params.get(e).getCE() > 0) ? params.get(e).getCEF(f) / params.get(e).getCE() : 0);
						j++;
					}
					i++;
				}
				k++;
			}
			for(String e : params.keySet()){
				params.get(e).reset();
			}
		}
		
		return params;
	}

	public static void printTop10(String word, HashMap<String, EMRecord> params){
		stdout.println(word + ":");
		int i = 0;
		for(EMParam1 em : params.get(word).sort()){
			if(i == 10)
				break;
			stdout.println(em.getWord() + " " + em.tParam);
			i++;
		}
		stdout.println();
	}

	public static void printAlignment(String eline, String fline, HashMap<String, EMRecord> params){
		String[] fWords = fline.split(" ");
		String[] eWords = ("_NULL_ "+eline).split(" ");//make sure to get _NULL_ in there
		int[] a = new int[fWords.length];
		for(int i = 0; i < fWords.length; i++){
			double maxT = 0;
			for(int j = 0; j < eWords.length; j++){
				double t = params.get(eWords[j]).getT(fWords[i]);
				if(t > maxT){
					a[i] = j;
					maxT = t;
				}
			}
		}
		stdout.print("[");
		for(int i : a){
			stdout.print(i+",");
		}
		stdout.println("]");
	}

	public static void main(String[] args) throws IOException{
		if(args.length != 4 || !args[3].equals("top10") && !args[3].equals("align")){
			stdout.println("usage: java Prob4 <english_corpus> <german_corpus> <test_words> <operation ('top10' or 'align')>");
			return;
		}
		//make readers for english and german corpora
		eFName = args[0];
		fFName = args[1];
		tFName = args[2];
		HashMap<String, EMRecord> params = emAlg(5);
		if(args[3].equals("top10")){
			//go through the test_words file, printing top 10
			BufferedReader testFile = new BufferedReader(new FileReader(tFName));
			String line;
			while((line = testFile.readLine()) != null){
				printTop10(line, params);
			}
		}
		else{
			BufferedReader engFile = new BufferedReader(new FileReader(eFName));
			BufferedReader forFile = new BufferedReader(new FileReader(fFName));
			String eline, fline;
			for(int i = 0; i < 20; i++){
				printAlignment(engFile.readLine(), forFile.readLine(), params);
			}
		}
	}
}