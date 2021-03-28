package com.collection;

public class FindSequence {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		printAll(4);
	}
	
	public static void printAll(int k) {
		int count = 0;
		int a[] = new int[k];
		
		for(int i = 0;i< k; i++) {
			a[i]=1;
		}
		int currentSum = 0;
		a[1] = 0;
		for(int i = 0;i< k; i++) {
			a[1]++;
			for(int j = 0; j<k-i;j++) {
				currentSum += a[i];
				count++;
				
				if(currentSum == k) {
					for(int m = 0; m < count;m++) {
						System.out.println(a[m]+ "");
					}
					System.out.println();
				}
			}
			count = 0;
		}
		
	}

}
