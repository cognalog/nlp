import java.util.ArrayList;
import java.util.HashMap;
import java.io.*;

public class Prob4{
	static BufferedReader engFile;
	static BufferedReader forFile;
	static String eFName;
	static String fFName;
	static PrintStream stdout = System.out;

	private static void resetReaders() throws FileNotFoundException{
		engFile = new BufferedReader(new FileReader(eFName));
		forFile = new BufferedReader(new FileReader(fFName));
	}

	/*
	* gives an initial value for t(f | e) for a particular e regardless of f
	*/
	private static double initialT(String word) throws IOException{
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
	public static HashMap<String, HashMap<String, Double>> emAlg(int iterations){

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
		resetReaders();
		stdout.println(initialT("resumption"));
	}
}