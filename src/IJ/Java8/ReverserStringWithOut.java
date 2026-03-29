package com.async.Java8;

public class ReverserStringWithOut {
    public static void main(String[] args) {
        String str = "Hello";
        String reversedStr = reverseString(str);
        System.out.println("Reversed String: " + reversedStr);
    }

    public static String reverseString(String str) {
//        char[] charArray = str.toCharArray();
//        String reversed = "";
//        for (int i = charArray.length - 1; i >= 0; i--) {
//            reversed += charArray[i];
//        }
//        return reversed;

//        String reversed = "";
//        for (int i = str.length() - 1; i >= 0; i--) {
//            reversed += str.charAt(i);
//        }
//        return reversed;

        if (str.isEmpty()) {
            return str; // Base case: an empty string is its own reverse
        } else {
            // Recursive call: return the reversed substring (from index 1)
            // plus the first character of the original string
            return reverseString(str.substring(1)) + str.charAt(0);
        }
    }
}