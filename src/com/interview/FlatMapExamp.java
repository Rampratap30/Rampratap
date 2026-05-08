package com.interview;

import java.util.Arrays;
import java.util.List;

public class FlatMapExamp {
    public static void main(String[] args) {
        List<List<Integer>> listOfStream = Arrays.asList(
                Arrays.asList(1,2,3),
                Arrays.asList(4,5),
                Arrays.asList(6,7,8)
        );

        System.out.println(listOfStream);

        List<Integer> flatMapsRes = listOfStream.stream().flatMap(List::stream).toList();

        System.out.println(flatMapsRes);

    }
}
