import java.util.*;

public class EM2Result{
	public double[][][][] qParams;
	public HashMap<String, EMRecord> tParams;

	public EM2Result(double[][][][] q, HashMap<String, EMRecord> t){
		qParams = q;
		tParams = t;
	}

	public String argMaxAlignment(String eline, String fline){
		String[] fWords = fline.split(" ");
		String[] eWords = ("_NULL_ "+eline).split(" ");//make sure to get _NULL_ in there
		int[] a = new int[fWords.length];
		for(int i = 0; i < fWords.length; i++){
			double maxT = 0;
			for(int j = 0; j < eWords.length; j++){
				double tq = tParams.get(eWords[j]).getT(fWords[i]) * qParams[eWords.length][fWords.length][j][i];
				if(tq > maxT){
					a[i] = j;
					maxT = tq;
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

	public double maxAlignment(String eline, String fline){
		String[] fWords = fline.split(" ");
		String[] eWords = ("_NULL_ "+eline).split(" ");
		double total = 0;
		for(int i = 0; i < fWords.length; i++){
			double maxT = 0;
			for(int j = 0; j < eWords.length; j++){
				double q = qParams[eWords.length][fWords.length][j][i];
				double tq = tParams.containsKey(eWords[j]) &&  tParams.get(eWords[j]).getT(fWords[i]) > 0 ? tParams.get(eWords[j]).getT(fWords[i]) * q	: q * q;
				if(tq > maxT)
					maxT = tq;
			}
			//maxT is now the highest q*t for a matching english word
			total += (maxT > 0) ? -1 * Math.log(maxT) : -999999;
		}

		return total;
	}
}