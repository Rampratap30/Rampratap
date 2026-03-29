package com.async.leetcode.easy;

public class PalindromeNumber {
    public static void main(String[] args) {
        int str= 333;
        boolean test = palindrome_Number(str);
        System.out.println(test);
    }
    private static boolean palindrome_Number(int str) {
        String original = Integer.toString(str);
        String reversed = new StringBuilder(original).reverse().toString();
        return original.equals(reversed);
    }

}
    
