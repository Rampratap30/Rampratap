package com.collection;

public class PerfectSumProblem {

	static void sum(int[] arr, int i, int sum, int target, String s)
	{   
	    for(int j = i+1; j<arr.length; j++){
	        if(sum+arr[j] == target){
	            System.out.println(s+" "+String.valueOf(arr[j]));
	        }else{
	            sum(arr, j, sum+arr[j], target, s+" "+String.valueOf(arr[j]));
	        }
	    }
	}
	
	/*
	 * public synchronized void m1() { } public synchronized void m2() { m1(); }
	 */
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int[] numbers = {6,3,8,10,1};
		
		int targetVal = 4;
	    for(int i =0; i<numbers.length; i++){
	        sum(numbers, i, numbers[i], targetVal, String.valueOf(numbers[i])); 
	    }
	    
		/*
		 * PerfectSumProblem s = new PerfectSumProblem(); s.m2();
		 * System.out.println("Done");
		 */

	}

}
