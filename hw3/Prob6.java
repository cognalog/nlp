import java.io.*;

public class Prob6{
	static final PrintStream stdout = System.out;

	public static void main(String[] args) throws IOException{
		if(args.length != 4){
			stdout.println("usage: java Prob6 <english_corpus> <foreign_corpus> <scrambled_english> <original_foreign>");
			return;
		}

		BufferedReader fReader = new BufferedReader(new FileReader(args[3]));
		EM2Result model = Prob5.emAlg(1, args[0], args[1]);

		stdout.println("Unscrambling...");
		double time = System.currentTimeMillis();
		String eline, fline;
		while((fline = fReader.readLine()) != null){
			BufferedReader eReader = new BufferedReader(new FileReader(args[2]));
			double max = 0;
			String maxE = "nothing to see here!";

			//get english sentence with the most probable alignment
			while((eline = eReader.readLine()) != null){
				double pAlign = model.maxAlignment(eline, fline);
				if(pAlign > max){
					max = pAlign;
					maxE = eline;
				}
			}
			stdout.println(maxE);
		}
		stdout.println((System.currentTimeMillis() - time) / 1000 + " seconds elapsed");
	}
}