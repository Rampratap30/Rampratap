import java.util.Arrays;
import java.util.stream.Stream;

public class UniqueWordCount {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		String txt = "apple banana orange apple banana";
		
		String[] words = txt.split("");
		
		System.out.println("Initial word count: " + words.length); 
		
		Stream<String> stream = Arrays.stream(words);
		
		long uniqueWords = stream.map(String::toLowerCase).distinct().count();
		System.out.println(uniqueWords);
	}

}
