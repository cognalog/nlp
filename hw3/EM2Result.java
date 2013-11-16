import java.util.*;

public class EM2Result{
	public double[][][][] qParams;
	public HashMap<String, EMRecord> tParams;

	public EM2Result(double[][][][] q, HashMap<String, EMRecord> t){
		qParams = q;
		tParams = t;
	}

	public String maxAlignment(String eline, String fline){
		String[] fWords = fline.split(" ");
		String[] eWords = ("_NULL_ "+eline).split(" ");//make sure to get _NULL_ in there
		int[] a = new int[fWords.length];
		for(int i = 0; i < fWords.length; i++){
			double maxT = 0;
			for(int j = 0; j < eWords.length; j++){
				double t = tParams.get(eWords[j]).getT(fWords[i]) * qParams[eWords.length][fWords.length][j][i];
				if(t > maxT){
					a[i] = j;
					maxT = t;
				}
			}
		}

		//stringify that ho
		String result = "[ ";
		for(int i : a){
			result += i+" ";
		}
		result += "]";

		return result;
	}
}