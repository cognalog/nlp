public class EMParam1{
	public double tParam;
	public double cef;

	public EMParam1(){
		tParam = 0;
		cef = 0;
	}

	public String toString(){
		return "c(f,e):"+cef+", t(f|e):"+tParam;
	}
}