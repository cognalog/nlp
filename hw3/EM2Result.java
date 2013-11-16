import java.util.*;

public class EM2Result{
	public double[][][][] qParams;
	public HashMap<String, EMRecord> tParams;

	public EM2Result(double[][][][] q, HashMap<String, EMRecord> t){
		qParams = q;
		tParams = t;
	}
}