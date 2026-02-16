package com.hexaware;

import java.util.Arrays;
import java.util.IntSummaryStatistics;

public class ArrayStatistics {

	public static void main(String[] args) {
		
		int[] numbers = {10, 25, 8, 42, 17, 30};
		
		

		// Get the IntSummaryStatistics object in a single stream pipeline
        IntSummaryStatistics stats = Arrays.stream(numbers).summaryStatistics();

        // Retrieve the individual values
        long count = stats.getCount();
        int min = stats.getMin();
        int max = stats.getMax();
        long sum = stats.getSum();
        double average = stats.getAverage();

        // Print the results
        System.out.println("Array of numbers: " + Arrays.toString(numbers));
        System.out.println("Count: " + count);
        System.out.println("Minimum: " + min);
        System.out.println("Maximum: " + max);
        System.out.println("Sum: " + sum);
        System.out.println("Average: " + average);

	}

}
