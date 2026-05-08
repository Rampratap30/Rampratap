package com.interview;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ShiftEvenOddNumber {
    public static void main(String[] args) {
        List<Integer> listNumber = List.of(1,2,3,4,5,6,7,8,9);

        Map<Boolean, List<Integer>> partitionList = listNumber.stream()
                .collect(Collectors.partitioningBy(x->x%2==0));

        List<Integer> evenNumber = partitionList.get(true);
        List<Integer> oddNumber = partitionList.get(false);

        System.out.println("EvenNumber ::"+ evenNumber+" OddNumber ::"+oddNumber);

    }
}
