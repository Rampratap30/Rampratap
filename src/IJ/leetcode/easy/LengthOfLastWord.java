package com.async.leetcode.easy;

public class LengthOfLastWord {
    public static void main(String[] args) {
        String str = "Hello World";
        // Trim trailing/leading spaces and split the string by spaces
        String [] words= str.trim().split(" ");

        //Get the last word from the resulting array
        String lastWorld = words[words.length-1];

        System.out.println(lastWorld.length());
    }
}
