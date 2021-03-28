package com.streamapi;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.function.Function;
import java.util.stream.Collectors;

//Group by a List and display the total count of it.
public class StremAPIGroupBy {

	public static void main(String[] args) {
		//3 apple, 2 banana, others 1
        List<String> items =
                Arrays.asList("apple", "apple", "banana",
                        "apple", "orange", "banana", "papaya");
        
        Map<String, Long> result =
                items.stream().collect(Collectors.groupingBy(Function.identity(),Collectors.counting()));
        
        System.out.println(result);
        Map<String,Long> ordering = new TreeMap<String,Long>(result);
        System.out.println("Ascending order :: " + ordering);
        
        Map<String,Long> reverseSortedMap = new TreeMap<String,Long>(Collections.reverseOrder());
        
        reverseSortedMap.putAll(ordering);
        
        System.out.println("Descending order :: " + reverseSortedMap);
        
        Set<String> setWithoutDuplicates  = items.stream().collect(Collectors.toSet());
        
        System.out.println(setWithoutDuplicates);
        
                
                

	}

}
