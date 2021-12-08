import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class UniqueWordCount {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		String txt = "apple banana orange apple banana";
		
		String[] words = txt.split("");
		
		//System.out.println("Initial word count: " + words.length);
		
		Stream<String> stream = Arrays.stream(words);
		
		long uniqueWords = stream.map(String::toLowerCase).distinct().count();
		//System.out.println(uniqueWords);

		String aaa = "Middle English storie, from Medieval Latin historia narrative, illustration, story of a building, " +
				"from Latin, history, tale; probably from narrative friezes on the window level of medieval buildings tale;";
		//String[] stringarray = aaa.split("[\\s,;]+");

		Map<String , Long> map =  Arrays.stream(aaa.split("[\\s,;]+")).collect(Collectors.groupingBy(c -> c , Collectors.counting()));
		map.forEach( (k, v) -> System.out.println(k + "  "+ v +" times "));


		int nums[] = {1,4,3,2,6,7,4,2,-1,2,8,6,7};

		List<Integer> integer = Arrays.stream(nums).boxed().collect(Collectors.toList());

		System.out.println(" ");
		integer.forEach(System.out::print);
		integer.sort(Integer::compareTo);
		System.out.println(" ");
		System.out.println("Sorted! ::");
		integer.forEach(System.out::print);
	}

}
