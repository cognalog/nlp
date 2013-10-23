import org.json.simple.*;
import org.json.simple.parser.*;
import java.io.*;

public class Prob4{
	public static void main(String[] args){
		if(args.length < 1){
			System.out.println("usage: java Prob4 <training_file>");
			return;
		}
		try{
			FileReader trainFR = new FileReader(args[0]);
			BufferedReader trainBR = new BufferedReader(trainFR);
			String line = null;
			JSONParser parser = new JSONParser();
			while((line = trainBR.readLine()) != null){
				JSONArray tree = (JSONArray)parser.parse(line);
				System.out.println(tree.get(1));
				break;
			}
			trainFR.close();
		}catch(Exception e){
			System.out.println(e);
		}
	}
}