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
	private static double initialT(String word) throws IOException{
		BufferedReader engFile = new BufferedReader(new FileReader(eFName));
		BufferedReader forFile = new BufferedReader(new FileReader(fFName));
		ArrayList<Integer> lines = new ArrayList();
		HashMap<String, Integer> emissions = new HashMap();
		String line;
		
		int i= 0;
		//find which english corpus lines contain the word
		while((line = engFile.readLine()) != null){
			if(line.indexOf(word) > -1)
				lines.add(i);
			i++;
		}
		/*
		* now, get dupeless list of all german words on those lines
		* the i variable now keeps track of your place in the lines list
		*/
		i = 0;
		int j = 0;
		while((line = forFile.readLine()) != null){
			if(i < lines.size() && j == lines.get(i) || word.equals("_NULL_")){
				String[] words = line.split(" ");
				for(String f : words){
					emissions.put(f, 0);
				}
				i++;
			}
			j++;
		}
		return (emissions.size() > 0) ? 1.0 / emissions.size() : 0;
	}
/*
	public static HashMap<String, HashMap<String, Double>> emAlg(int iterations) throws IOException{
		HashMap<String, HashMap<String, Double>> params = new HashMap();
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
						double t = initialT(e);

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
	}
}