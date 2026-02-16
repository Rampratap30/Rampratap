package com.hexaware;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class RemoveDuplicate {

	public static void main(String[] args) {
		
		ArrayList<Integer> numbers = new ArrayList<>(Arrays.asList(1, 2, 3, 2, 4, 1, 5));
		
		List<Integer> list = new ArrayList<>(numbers);
		
		List<Integer> removeDuplicates= list.stream().distinct().collect(Collectors.toList());
		
		System.out.println("List after removing duplicates: " + removeDuplicates);
		
		List<Integer> reverseOrder = removeDuplicates.stream().sorted((a, b) -> b.compareTo(a)).collect(Collectors.toList());
		
		System.out.println("List in reverse order: " + reverseOrder);
	}

}
