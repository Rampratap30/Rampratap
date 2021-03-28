package com.program;

public class BubbleSort {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int arr[] = {860,3,200,9};
		System.out.println("--Array Befor Bubble Sort----");
		
		printArray(arr);
		bubbleSort(arr);

	}

	private static void bubbleSort(int[] arr) {
		// TODO Auto-generated method stub
		
		int temp = 0;
		
		for(int i=0;i<arr.length;i++) {
			System.out.println("Sort Pass Number "+(i+1));
			for(int j = 1; j<(arr.length-i);j++) {
				System.out.println("Comparing "+ arr[j-1]+ " and " + arr[j]);
				if(arr[j-1]> arr[j]) {
					//swap element
					temp= arr[j-1];
					arr[j-1] = arr[j];
					arr[j] = temp;
					
					System.out.println(arr[j]  + " is greater than " + arr[j-1]);
				    System.out.println("Swapping Elements: New Array After Swap");
				    
				    printArray(arr);
					
				}
				
			}
		}		
	}

	private static void printArray(int[] arr) {
		// TODO Auto-generated method stub
		
		for(int i = 0; i < arr.length;i++) {
			System.out.println(arr[i] +"");
		}
		System.out.println();
		
	}

}
