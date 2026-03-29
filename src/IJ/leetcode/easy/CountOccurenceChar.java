package com.async.leetcode.easy;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class CountOccurenceChar {
    public static void main(String[] args) {
        String str = "geeksforgeeks";
        char ch = 'e';

        System.out.println(countResult(str,ch));

        long counts = str.chars().filter(c->c==ch).count();
        System.out.println(counts);

        List<Integer> lists = Arrays.asList(217, 317, 417, 517);
        lists.stream().sorted(Comparator.reverseOrder()).forEach(System.out::println);

        List<Integer> results = lists.stream().sorted(Comparator.reverseOrder()).collect(Collectors.toList());
        System.out.println(results);



    }

    private static long countResult(String str, char ch) {
        return str.chars().filter(c->c==ch).count();
    }
}

