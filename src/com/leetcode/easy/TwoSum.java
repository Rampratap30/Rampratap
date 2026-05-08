package com.leetcode.easy;

import java.util.HashMap;

public class TwoSum {

	public static void main(String[] args) {
		int[] arr= {1,2,3,4,5};
		int target = 8;

		for (int i : targetTwoSum(arr,target)) {System.out.print(i+" ");}

	}
	//Brute Force Approach
	// This approach achieves O(n*n) due to two nested loop Time Complexity and O(1) Space Complexity.
	private static int[] twoSum(int [] nums, int target) {
		//int[] a = new int[2];
		for (int i = 0; i < nums.length; i++) {
			for (int j = i + 1; j < nums.length; j++) {
				if (nums[i] + nums[j] == target) {
					return new int[]{i,j};
				}
			}
		}
		return new int[]{0,0};
	}

	//Time Complexity: O(n)because we traverse the list containing elements only once.
	//Space Complexity:O(n) for the extra space required by the hash map.
	static int[] targetSum(int[] nums, int target) {
		if(nums == null || nums.length < 2) {
			return new int[]{0, 0};
		}
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

	//Two sum ii input array is sorted
	/*
	This approach achieves O(n) Time Complexity and O(1) Space Complexity.
	*/

	private static int[] targetTwoSum(int[] numbers, int target){
		int left = 0;
		int right = numbers.length-1;
		while (left < right){
			int sum = numbers[left]+numbers[right];
			if(sum == target){
				return new int[]{left+1, right+1};
			}else if(sum < target){
				left++;
			}else{
				right--;
			}
		}
		return new int[]{-1,-1};
	}

}
