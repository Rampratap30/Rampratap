import java.util.Scanner;

public class Problem1 {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        // input for word1
        String word1 = in.nextLine();

        // input for word2
        String word2 = in.nextLine();

        int result = isSameReflection(word1, word2);
        System.out.print(result);
    }

    private static int isSameReflection(String word1, String word2) {

        // Write your code here
        if(word1.length() != word2.length()){
            return -1;
        }
        return (word1 + word1).contains(word2) ? 1 : -1;
    }
}
