package com.interview;

import java.util.Comparator;
import java.util.List;

public class LongestString {
    public static void main(String[] args) {
        List<String> words = List.of("Java", "Spring", "Kubernetes","AI","Microservices","Docker","API");

        String longestWord = words.stream().max(Comparator.comparingInt(String:: length)).orElse("");
        System.out.println(longestWord);
    }
}
