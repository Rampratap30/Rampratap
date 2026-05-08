package com.leetcode;

import java.util.HashMap;

public class Target_sum {
    public static void main(String[] args)
    {
        int [] a = {3,3};
        int target = 6;

        for(int x : targetSum(a , target))
            System.out.print(x + " ");

    }

    static int[] targetSum(int[] nums, int target) {
        if(nums==null || nums.length<2)
            return new int[]{0,0};

        HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
        for(int i=0; i<nums.length; i++){
            if(map.containsKey(nums[i])){
                return new int[]{map.get(nums[i]), i};
            }else{
                map.put(target-nums[i], i);
            }
        }
        return new int[]{0,0};
    }
}
