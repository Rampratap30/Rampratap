package com.interview;

import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class FindMissingNumber {
    public static void main(String[] args) {

        int[] arr={1,2,1,2,5,8};

        int min = Arrays.stream(arr).min().getAsInt();
        int max = Arrays.stream(arr).max().getAsInt();

        Set<Integer> collect = Arrays.stream(arr).boxed().collect(Collectors.toSet());

        List<Integer> list= IntStream.rangeClosed(min,max).boxed().
                filter(x->!collect.contains(x)).toList();

        System.out.println(list);

        //Missing one number in Array
        int[] numbers = {1, 2, 4, 5, 6};

        int n = numbers.length + 1;//Total Numbers should be present.

        int expectSum = n*(n+1)/2;
        int actualSum = Arrays.stream(numbers).sum();
        
        int finalMissNumber = expectSum - actualSum;
        System.out.println(finalMissNumber);


    }

}
