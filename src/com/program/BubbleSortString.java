package com.program;

public class BubbleSortString {

	public static void main(String[] args) {
		String str[] = { "AB", "ABC", "AB", "ABCD", "ABC"};
		String temp;
		System.out.println("Strings in sorted order:");
		for (int j = 0; j < str.length; j++) {
	   	   for (int i = j + 1; i < str.length; i++) {
			// comparing adjacent strings
			if (str[i].compareTo(str[j]) < 0) {
				temp = str[j];
				str[j] = str[i];
				str[i] = temp;
			}
		   }
		   System.out.println(str[j]);
		}
		
		int arr[] = {120,110,100,19};
		int temps = 0;
		int n = arr.length;
		
		System.out.println("Integer in sorted order ::");
		for(int i= 0; i<n;i++) {
			for(int j = 1; j<(n-i);j++) {
				if(arr[j-1]<arr[j]) {
					temps = arr[j-1];
					arr[j-1] = arr[j];
					arr[j] = temps;					
				}
			}
		}
		 for(int i=0; i < arr.length; i++){  
             System.out.print(arr[i] + " ");  
     }
		
		

	}
}
