package com.program;

import java.util.Arrays;

public class MargeArrayProgram {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int[] arrayA = {12,-7,18,9, 37,-1,21};
		int[] arrayB = {27,8,71,-9,18};
		
		int[] mergeArray = mergeArray(arrayA, arrayB);
	
		System.out.println("Array A :: " + Arrays.toString(arrayA));		
		System.out.println("Array B :: " + Arrays.toString(arrayB));
		System.out.println("MergeArray :: " + Arrays.toString(mergeArray));
	}

	private static int[] mergeArray(int[] arrayA, int[] arrayB) {
		// TODO Auto-generated method stub
		
		int[] mergedArray = new int[arrayA.length+arrayB.length];
		
		int i=0, j=0,k=0;
		
		while(i<arrayA.length) {
			mergedArray[k] = arrayA[i];
			i++;
			k++;
		}
		
		while(j<arrayB.length) {
			mergedArray[k] = arrayB[j];
			j++;
			k++;
		}
		
		Arrays.sort(mergedArray);
		
		return mergedArray;
	}

}
