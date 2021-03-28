package com.collection;

public class GetmNumberOfSubsets {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int [] arr = {9,3,6,2,2,12};
		
		int target = GetmNumberOfSubsetss(arr,9);
		
		System.out.println(target);
		

	}
	
	private static int GetmNumberOfSubsetss(int[] numbers, int sum)
	{
	    int[] dp = new int[sum + 1];
	    dp[0] = 1;
	    int currentSum =0;
	    for (int i = 0; i < numbers.length; i++)
	    {
	        currentSum += numbers[i];
	        for (int j = Math.min(sum, currentSum); j >= numbers[i]; j--)
	            dp[j] += dp[j - numbers[i]];
	    }

	    return dp[sum];
	}

}
