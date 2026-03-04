package com.leetcode.easy;

public class TwoSum {

	public static void main(String[] args) {
		 int[] arr= {2,7,11,15};
	        int target = 9;

	        int [] result = twoSum(arr,target);
	        for (int i : result) {
	        
	        				System.out.println(i);}
	        

	}
	
	private static int[] twoSum(int [] nums, int target) {
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
	}

}
