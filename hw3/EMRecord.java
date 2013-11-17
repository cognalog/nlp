import java.util.*;

public class EMRecord{
	HashMap<String, EMParam1> dict;
	double ce;

	public EMRecord(){
		dict = new HashMap();
		ce = 0;
	}

	public List<EMParam1> sort(){
		List<EMParam1> emrs = new ArrayList<EMParam1>(dict.values());
		Collections.sort(emrs, new Comparator<EMParam1>(){
			public int compare(EMParam1 em1, EMParam1 em2){
				if(em1.tParam > em2.tParam)
					return -1;
				else if(em1.tParam < em2.tParam)
					return 1;
				else
					return 0;
			}
		});
		return emrs;
	}

	public int size(){ return dict.size(); }

	public double getCE(){ return ce; }

	public double getCEF(String f){ return dict.get(f).cef; }

	public HashMap<String, EMParam1> getDict() { return dict; }

	public double getT(String key){ return dict.get(key).tParam; }

	public void set(String key, EMParam1 value){ dict.put(key, value); }

	public void updateT(String f, double value){
		dict.get(f).tParam = value;
	}

	public void setTs(){
		for(String f : dict.keySet()){
			dict.get(f).tParam = 1.0 / dict.size();
		}
	}

	public void increment(String f, double by){
		ce += by;
		dict.get(f).cef += by;//fun fact: I spent hours on semantic debugging when this += was a = all along
	}

	public void reset(){
		ce = 0;
		for(String f : dict.keySet()){	
			dict.get(f).cef = 0;
		}
	}

	public String toString(){
		return "[c(e):"+ce+", "+dict.toString()+"]";
	}

}