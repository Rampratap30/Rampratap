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

        //For sorting
        List<Integer> sorted = integersList.stream().distinct().sorted().collect(Collectors.toList());
        System.out.println(sorted);

        int[] nums ={3,2,2,3};
        int result = removeElement(nums,3);

        System.out.println(result);
    }

    public static int removeElement(int[] nums, int val) {
        int k = 0;
        for (int x : nums) {
            if (x != val) {
                nums[k++] = x;
            }
        }
        return k;
    }
}
