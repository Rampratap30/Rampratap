package com.Wissen;

import java.util.Arrays;
import java.util.Comparator;

public class LongestEvenLength {
    public static void main(String[] args) {
        String sentence = "problem input for the sample";

        String arr[] = sentence.split("\\s+");

        int len = 0;
        String word = "";
        for (int i= 0; i< arr.length; i++) {
            if((arr[i].length())%2 ==0){
                int len1 = arr[i].length();
                if(len1>len){
                    len = len1;
                    word = arr[i];
                }
            }
        }
        System.out.println(word);

        String longestWord = Arrays.stream(sentence.split(" ")) // creates the stream with words
                .filter(s -> s.length() % 2 == 0) // filters only the even length strings
                .max(Comparator.comparingInt(String::length)) // finds the string with the max length
                .orElse(" "); // returns " " if none string is found

        System.out.println(longestWord);
    }


}
