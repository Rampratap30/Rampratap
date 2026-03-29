package com.async.leetcode.easy;

public class LongestPalindromeString {
    public static void main(String[] args) {
        String str="babad";

        String results= longestPalindrome(str);
        System.out.println(results);

    }

    private static String longestPalindrome(String str) {
        if(str  == null || str.length()< 1) return "";
        int n = str.length();
        String longest="";
        for(int i=0;i<n;i++){
            for (int j=1;j<n;j++){
                if(isPalindrome(str,i,j) && (j-i+1)> longest.length()){
                    longest= str.substring(i,j+1);
                }
            }
        }
        return longest;
    }

    private static boolean isPalindrome(String str, int i, int j) {
        if(i<j){
            if(str.charAt(i) !=str.charAt(j)){
                return false;
            }else{
                i++;
                j--;
            }
        }
        return true;
    }
}
