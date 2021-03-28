package com.program;

import java.util.Arrays;

public class BinarySearch {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int intArr[] = {10,20,30,40,50};
		int intKey = 20;
		
		//int last = intArr.length-1;
		
		//System.out.println(last);
		
		//binarySearch(intArr,0,last,intKey);
		
		//Arrays.sort(intArr);
		
		int result = Arrays.binarySearch(intArr,intKey);
		if(result < 0) {
			System.out.println("Element is not found");
		}else {
			System.out.println(intKey + " found at index = "
	                +Arrays.binarySearch(intArr,intKey));
		
		}

	}

	/*
	 * private static void binarySearch(int[] intArr, int first, int last, int
	 * intKey) { // TODO Auto-generated method stub
	 * 
	 * int mid = (first+last)/2;
	 * 
	 * while(first<=last) { if(intArr[mid]< intKey) { first = mid+1; }else
	 * if(intArr[mid] == intKey) { System.out.println("Element found at index :: " +
	 * mid); break; }else { last = mid-1; } mid = (first+last)/2; }
	 * 
	 * if(first>last) { System.out.println("Element is not found ::"); }
	 * 
	 * 
	 * }
	 */
}
