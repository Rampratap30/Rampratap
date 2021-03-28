import java.nio.charset.Charset;
import java.util.Random;
import java.util.Scanner;

/*Author by Rampratap*/

public class GenerateAlphaNumericAndNumericString {

	final static String getAlphaNumericString(String randomString, int length) {

		// length is bounded by 1000 Character
		byte[] array = new byte[1000];
		new Random().nextBytes(array);

		randomString = new String(array, Charset.forName("UTF-8"));

		// Create a StringBuilder to store the result
		StringBuilder r = new StringBuilder();

		// Append first nth alphanumeric characters
		// from the generated random String into the result
		for (int k = 0; k < randomString.length(); k++) {

			char ch = randomString.charAt(k);

			if (((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') || (ch >= '0' && ch <= '9')) && (length > 0)) {

				r.append(ch);
				length--;
			}
		}
		return r.toString();
	}
	public static boolean isNumeric(final String str) {

        // null or empty
        if (str == null || str.length() == 0) {
            return false;
        }

        return str.chars().allMatch(Character::isDigit);

    }
	
	static String getNumericString(String inputString, int length) {
	       final String characters = "1234567890";
	       // Create a StringBuilder to store the result
	       StringBuilder result = new StringBuilder();
	       // Append first nth alphanumeric characters
	       // from the generated random String into the result
	       for (int k = 0; k < inputString.length(); k++) {
	    	   Random rand = new Random();
	           result.append(characters.charAt(rand.nextInt(characters.length())));
	           length--;
			}
	       return result.toString();
	    }

	public static void main(String[] args) {
		
		System.out.println("--------Please Enter  NumericString/AlphaNumericString -------- ");  
        Scanner in = new Scanner(System.in);  
        
        String inputString = in.next(); 
		
		int length = inputString.length();
		
		if(length > 0) {
		
			if(isNumeric(inputString)) {
				System.out.println(getNumericString(inputString, length));
	
			}else {
				System.out.println(getAlphaNumericString(inputString, length));
	
			}
		}
	}
}
