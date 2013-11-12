import java.util.ArrayList;
import java.util.HashMap;
import java.io.*;

public class Prob4{
	static BufferedReader engFile;
	static BufferedReader gerFile;
	static PrintStream stdout = System.out;

	public static double initialT(String word){
		ArrayList<Integer> lines = new ArrayList();
		HashMap<String, Integer> emissions = new HashMap();
		String line;
		int i= 0;
		int j = 0;

		try{
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
			while((line = gerFile.readLine()) != null){
				if(i < lines.size() && j == lines.get(i)){
					String[] words = line.split(" ");
					for(String f : words){
						emissions.put(f, 0);
					}
					i++;
				}
				j++;
			}
		}
		catch(IOException e){
			stdout.println(e);
			return 0;
		}
		return 1.0 / emissions.size();
	}

	public static void main(String[] args){
		if(args.length < 2){
			stdout.println("usage: java Prob4 <english_corpus> <german_corpus>");
			return;
		}
		try{
			//make readers for english and german corpora
			engFile = new BufferedReader(new FileReader(args[0]));
			gerFile = new BufferedReader(new FileReader(args[1]));	
		}
		catch(Exception e){
			System.out.println(e);
		}
	}
}