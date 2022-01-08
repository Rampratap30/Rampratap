package com.leetcode;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class RemoveDuplicate {
    public static void main(String[] args)
    {
        int [] a = {11,7,2,2,15,11};
        List<Integer> integersList = Arrays.stream(a).boxed().collect(Collectors.toList());
        System.out.println(integersList);

        List<Integer> sorted = integersList.stream().sorted().collect(Collectors.toList());
        System.out.println(sorted);

        List<Integer> removed = sorted.stream().distinct().collect(Collectors.toList());
        System.out.println(removed);
    }
}
