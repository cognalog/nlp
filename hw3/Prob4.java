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
					emissions.get("_NULL_").set(f, new EMParam1());
					emissions.get(e).set(f, new EMParam1());
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
						params.get(e).updateT(f, params.get(e).getCEF(f) / params.get(e).getCE());
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

	public static void main(String[] args) throws IOException{
		if(args.length < 2){
			stdout.println("usage: java Prob4 <english_corpus> <german_corpus>");
			return;
		}
		//make readers for english and german corpora
		eFName = args[0];
		fFName = args[1];
		HashMap<String, EMRecord> result = emAlg(1);
		stdout.println(result.get("roth"));
	}
}