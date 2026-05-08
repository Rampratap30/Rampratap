package com.leetcode.easy;

public class RemoveDuplicateArray2 {
    public static void main(String[] args) {
        int[] arr={1,1,1,2,2,3};

        int result = removeDuplicateArrayTwo(arr);
        System.out.println(result);
    }

    private static int removeDuplicateArrayTwo(int[] nums){
        int k=0;
        for(int n : nums){
            if(k<2|| n!= nums[k-2]){
                nums[k] = n;
                k++;
            }
        }
        return k;
    }
}
