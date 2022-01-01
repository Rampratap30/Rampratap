package com.leetcode;

import java.util.HashMap;

public class Target_sum {
    public static void main(String[] args)
    {
        int [] a = {2,7,11,15};
        int target = 9;

        for(int x : targetSum(a , target))
            System.out.print(x + " ");

    }

    static int[] targetSum(int[] nums, int target) {
       /* for(int i = 0 ; i <nums.length - 1 ; i++){
            for(int j = i  ; j < nums.length ; j++)
            {
                if(nums[i] + nums[j] == target)
                    return new int[]{i+1,j+1};
            }
        }
        return new int[]{-1 , -1};*/

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
