import java.util.HashMap;
import java.io.*;

public class Prob4{
	private static PrintStream stdout = System.out;
	public static void main(String[] args) throws IOException, InterruptedException{
		String[] hists = {"There DET", "is VERB", "no DET", "asbestos NOUN"};
		
		BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
  		
  		System.out.println("sup dawg");
  		int c;

  		while((c = stdin.read()) != -1){
  			System.err.print((char) c);
  		}
  		/*
		String out = "";
		for(String h : hists){
			histGenO.println(h);
			String in;			
			while((in = histGenI.readLine()) != null){
				stdout.println(in);
			}
		}
*/
		stdin.close();
	}
} 