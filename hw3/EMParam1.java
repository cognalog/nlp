public class EMParam1{
	String word;
	public double tParam;
	public double cef;

	public EMParam1(String w){
		word = w;
		tParam = 0;
		cef = 0;
	}

	public String getWord(){ return word; }

	public String toString(){
		return "c(f,e):"+cef+", t(f|e):"+tParam;
	}
}