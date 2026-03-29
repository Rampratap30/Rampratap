package com.async.leetcode.easy;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MergeTwoSortedLists {
    public static void main(String[] args) {

        List<Integer> number1 = Arrays.asList(1, 2, 4);
        List<Integer> number2    = Arrays.asList(1, 3, 5);

        List<Integer> result = mergeTwoLists(number1, number2);
        
        
    }

    private static List<Integer> mergeTwoLists(List<Integer> number1, List<Integer> number2) {

        List<Integer> finals = new ArrayList<>();
        if (number1 == null) {
            return number1;
        }
        if (number2 == null) {
            return number2;
        }
        return finals;
    }

}
