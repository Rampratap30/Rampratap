package com.collection;

import java.util.Arrays;

public class SecondLargestNew {

	public static void main(String[] args) {
		int[] array = { 0, 12, 74, 26, 82, 3, 89, 8, 94, 3,89 };

		int highest = Integer.MIN_VALUE;
		int secondHighest = Integer.MAX_VALUE;

		for (int i = 0; i < array.length; i++) {
			if (array[i] > highest) {
				// ...shift the current highest number to second highest
				secondHighest = highest;
				// ...and set the new highest.
				highest = array[i];
			} else if (array[i] > secondHighest) {
				// Just replace the second highest
				secondHighest = array[i];
			}
		}
		System.out.println("second largest is " + secondHighest);
		System.out.println("largest is " + highest);
		
		int[] randomIntegers = {1, 5, 4, 2, 8, 1, 1, 6, 7, 8, 9};
	    Arrays.sort(randomIntegers);
	    System.out.println(randomIntegers[randomIntegers.length-2]);
	}

}
