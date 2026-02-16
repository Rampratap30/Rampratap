package com.hexaware;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class RemoveEmptyArray {

	public static void main(String[] args) {
	
		List<String> listWithEmptyStrings = Arrays.asList("apple", "", "banana", " ", "", "cherry");

        // Remove empty strings
        List<String> listWithoutEmptyStrings = listWithEmptyStrings.stream()
                .filter(s -> s != null && !s.isBlank())
                .collect(Collectors.toList());

        System.out.println("Original list: " + listWithEmptyStrings);
        System.out.println("Filtered list: " + listWithoutEmptyStrings);
		
		

	}

}
