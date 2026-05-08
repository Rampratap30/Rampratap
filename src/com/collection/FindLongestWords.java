package com.collection;

import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class FindLongestWords {
    public static void main(String[] args) {
        String input = "The quick brown fox jumps over the lazy dog";
        String[] words = input.split(" ");
        String longestWord  = "";

        for(String word: words){
            if(word.length() > longestWord.length()){
                longestWord = word;
            }
        }
        System.out.println(longestWord);

        String longest = Arrays.stream(input.split(" "))
                .max(Comparator.comparingInt(String::length))
                .orElse("");

        System.out.println(longest);


        int[] arr = {1,2,3,4,5,6};
        List<Integer> list = Arrays.stream(arr).boxed().collect(Collectors.toList());
        System.out.println(list);
        Collections.reverse(list);
        System.out.println(list);

    }

}
