import java.io.*;
import java.util.HashMap;

public class Prob5{
	static PrintStream stdout = System.out;
	
	public static EM2Result emAlg(int iterations, String eFile, String fFile) throws IOException{
		double[][][][] qParams = new double[50][50][50][50]; //assumes max sentence length of 50 words
		HashMap<String, EMRecord> tParams = Prob4.emAlg(iterations, eFile, fFile);
		double[][][][] qCounts;
		stdout.println("Running IBM Model 2:");

		for(int its = 1; its <= iterations; its++){
			stdout.println("Starting iteration "+its);
			//reset all stored counts to 0
			for(String e : tParams.keySet()){
				tParams.get(e).reset();
			}
			qCounts = new double[50][50][51][50];

			//proceed to read
			BufferedReader eReader = new BufferedReader(new FileReader(eFile));
			BufferedReader fReader = new BufferedReader(new FileReader(fFile));
			String eline, fline;
			int k = 1;
			while((eline = eReader.readLine()) != null){
				if(k % 2000 == 0)
					stdout.println("on line "+k);
				String[] eWords = ("_NULL_ "+eline).split(" ");
				String[] fWords = fReader.readLine().split(" ");//assumes corpora are equally long
				//set some variables to make our lives easier
				int l = eWords.length;
				int m = fWords.length;
				double[][] qp = qParams[l][m];
				double[][] qc = qCounts[l][m];
				for(int i = 0; i < m; i++){
					//calculate denominator for delta
					double denom = 0;
					for(int j = 0; j < l; j++){
						if(qp[j][i] == 0)
							qp[j][i] = 1.0 / (l + 1);
						denom += qp[j][i] * tParams.get(eWords[j]).getT(fWords[i]);//assumes this t param has been calculated in Prob4
					}

					//estimate q and t params
					for(int j = 0; j < eWords.length; j++){
						String e = eWords[j];
						String f = fWords[i];
						//calculate delta
						double delta = (denom > 0) ? qp[j][i] * tParams.get(e).getT(f) / denom : 0;

						//increment counts by delta
						tParams.get(e).increment(f, delta);
						tParams.get(e).updateT(f, (tParams.get(e).getCE() > 0) ? tParams.get(e).getCEF(f) / tParams.get(e).getCE() : 0);
						qc[j][i] += delta; //c(j,i,l,m)
						qc[50][i] += delta; //c(i,l,m)

						//update q and t
						tParams.get(e).updateT(f, (tParams.get(e).getCE() > 0) ? tParams.get(e).getCEF(f) / tParams.get(e).getCE() : 0);
						qp[j][i] = qc[j][i] / qc[50][i];
					}
				}
				k++;
			}
		}
		//finally...
		return new EM2Result(qParams, tParams);
	}

	public static void main(String[] args) throws IOException{
		if(args.length != 2){
			stdout.println("usage: java Prob5 <english_corpus> <foreign_corpus>");
			return;
		}

		double time = System.currentTimeMillis();
		EM2Result params = emAlg(5, args[0], args[1]);
		stdout.println(params.tParams.get("resumption"));
		stdout.println((System.currentTimeMillis() - time) / 1000 + " seconds elapsed");

		//print best alignments for first 20 pairs
		BufferedReader engFile = new BufferedReader(new FileReader(args[0]));
		BufferedReader forFile = new BufferedReader(new FileReader(args[1]));
		for(int i = 0; i < 20; i++){
			stdout.println(params.maxAlignment(engFile.readLine(), forFile.readLine()));
		}
	}
}