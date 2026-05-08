package com.interview;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class OpusInterview {
    public static void main(String[] args) {
        int[] a = {2,6,1,9};
        int[] b = {4,3,8,7};

        List<Integer> list = Arrays.stream(a).boxed().toList();

        List<Integer> list1 = Arrays.stream(b).boxed().toList();

        List<Integer> list2 = new ArrayList<>();
            list2.addAll(list);
            list2.addAll(list1);

        List<Integer> finalResult = list2.stream().sorted().collect(Collectors.toList());

        System.out.println(finalResult);

        int[] result = IntStream.concat(IntStream.of(a), IntStream.of(b))
                .distinct() // Removes duplicates
                .sorted()   // Sorts the merged array
                .toArray();

        for (int i = 0; i <result.length ; i++) {
            System.out.println(result[i]);
        }
    }
}
