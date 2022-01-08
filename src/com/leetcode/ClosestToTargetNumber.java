package com.leetcode;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.stream.Collectors;

public class ClosestToTargetNumber {
    public static void main(String[] args)
    {
        int[] arr = new int[] { 2, 5, 6, 7, 8, 8, 9 };
        System.out.println(findClosest(arr, 11));


        List<Integer> list = Arrays.stream(arr).boxed().collect(Collectors.toList());

        int n = 11;

        int result = list.stream()
                .min(Comparator.comparingInt(i -> Math.abs(i - n)))
                .orElseThrow(() -> new NoSuchElementException("No value present"));

        System.out.println(result);
    }

    private static int findClosest(int[] arr, int target) {
        int idx = 0;
        int dist = Math.abs(arr[0] - target);
        for (int i = 1; i< arr.length; i++) {
            int cdist = Math.abs(arr[i]-target);

            if(cdist < dist){
                idx = i;
                dist = cdist;
            }
        }
        return arr[idx];

    }
}
