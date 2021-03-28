package com.streamapi;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;

public class RepeatingWordCount {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String str = "Roopa Roopi loves green color Roopa Roopi";
		
		Map<String, Long> map = Arrays.stream(str.split(" ")).
				collect(Collectors.groupingBy(Function.identity(),Collectors.counting()));
		
		System.out.println(map);
		
		//1. All string value with their occurrences
		Map<String, Long> counterMap  = Arrays.stream(str.split(" ")).
				collect(Collectors.groupingBy(e->e,Collectors.counting()));
		
		System.out.println(counterMap);
		
		//3. List of Duplicating Strings
	    List<String> masterStrings = Arrays.asList(str.split(" "));
	    Set<String> duplicatingStrings = 
	            masterStrings.stream().filter(i -> Collections.frequency(masterStrings, i) > 1)
	            .collect(Collectors.toSet());

	    System.out.println(duplicatingStrings);
	}

}
