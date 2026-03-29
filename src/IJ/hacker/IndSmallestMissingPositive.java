package com.async.hacker;

import java.util.*;

//Find the Smallest Missing Positive Integer
public class IndSmallestMissingPositive {
    public static void main(String[] args) {
        List<Integer> inputArr = Arrays.asList(3, 4, -1, 1);

        int countResult = indSmallestMissingPositives(inputArr);
        System.out.println(countResult);
    }

    private static int indSmallestMissingPositives(List<Integer> inputArr) {
        if(inputArr == null || inputArr.size()==0){
            return 0;
        }
        Set<Integer> numSet = new HashSet<>();
        // Step 1: Add all positive numbers to the set
        for (int num : inputArr) {
            if (num > 0) {
                numSet.add(num);
            }
        }

        // Step 2: Find the smallest missing positive number
        for (int i = 1; i <= inputArr.size(); i++) {
            if (!numSet.contains(i)) {
                return i;
            }
        }

        // Step 3: If all numbers from 1 to n are present
        return inputArr.size() + 1;
//        Collections.sort(inputArr);
//        int smallest = 1;
//        for (int i = 0; i <inputArr.size() ; i++) {
//            if(inputArr.get(i)==smallest){
//                smallest++;
//            }
//        }
//        return smallest;
    }
}
