package com.async.Java8;

public class FindVowels {
    public static void main(String[] args) {
        String str="rmk";

        System.out.println(findVowels(str));
    }

    private static boolean findVowels(String str) {
        return str.toLowerCase().matches(".*[aeiou].*");

    }
}
