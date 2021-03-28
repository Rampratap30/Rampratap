import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class TotalSum {

	public static void main(String[] args) {
		/*
		 * List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6);
		 * 
		 * int minValue =
		 * numbers.stream().min(Comparator.comparing(Integer::valueOf)).get();
		 * 
		 * System.out.println("Minimum Value ::"+minValue);
		 * 
		 * int maxValue =
		 * numbers.stream().max(Comparator.comparing(Integer::valueOf)).get();
		 * 
		 * System.out.println("Maxmum Value ::"+maxValue);
		 */
		 
		//System.out.print(sumAll(numbers));
 
		//int total = numbers.stream().mapToInt(i -> i.intValue()).sum();
		//System.out.print(total);
		
		/*
		 * int total = numbers.stream().mapToInt(value -> value).sum();
		 * System.out.print(total);
		 * 
		 * total = numbers.stream().mapToInt(Integer::intValue).sum();
		 * System.out.print(total);
		 */
		/*
		 * ArrayList l = new ArrayList(2); l.add(1); l.add(1); l.add(1);
		 * System.out.println(l.size());
		 */
		
		/*
		 * String a = null; String b = "Test"; Boolean c = a.equals(b);
		 * System.out.println(c);
		 *
		 */
		
		float f = (1/4)*10;
		int i = Math.round(f);
		System.out.println(i);

	}
	
	public static int sumAll(List<Integer> numbers) {
		int total = 0;
		for (int number : numbers) {
			total += number;
		}
		return total;
	}

}
