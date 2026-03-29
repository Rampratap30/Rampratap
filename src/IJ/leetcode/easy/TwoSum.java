package com.async.leetcode.easy;

import java.util.HashMap;
import java.util.Map;

public class TwoSum {
    public static void main(String[] args) {
        int[] arr= {2,7,10,13};
        int target = 17;

        int [] result = twoSum(arr,target);
        for (int i=0;i < result.length;i++){
            System.out.print(result[i]+" ");
        }
    }


    public static int[] twoSum(int[] nums, int target){
        //The Brute Force approach is simple but the least efficient with a time complexity of O(n2) and space complexity of O(1).
        int[] a = new int[2];
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    a[0] = i;
                    a[1] = j;
                }
            }
        }
        return a;

        //The One-Pass Hash Table approach is the most efficient with O(n) time complexity and O(n) space complexity,
        // as it optimizes the time by reducing the number of iterations over the array to one

        /*Step 1: Again, a map is created to store numbers and their indices.
         Step 2: During iteration over the numbers, the complement is calculated for each number.
         Step 3: It checks if the complement exists in the map. If so, the indices are returned.
         Step 4: Otherwise, the current number and its index are added to the map.
         Step 5: If no pair sums up to the target, null is returned.*/

//        Map<Integer, Integer> numMap = new HashMap<>();
//        for(int i=0;i< nums.length;i++){
//            int complement = target-nums[i];
//            if(numMap.containsKey(complement)){
//                return new int[]{numMap.get(complement),i};
//            }else{
//                numMap.put(nums[i], i);
//            }
//
//        }
//        return null;
    }


}
