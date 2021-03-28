package com.collection;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class RemoveDupElements {

	//function to remove duplicate from ArrayList
	public static<T> ArrayList<T> removeDuplicates(ArrayList<T> list) {
		
		//create a new ArrayList
		/*ArrayList<T> newlists = new ArrayList<T>();
		
		//Traverse through the first list
		for (T element : list) {
			if(!newlists.contains(element)) {
				newlists.add(element);
			}			
		}
		
		
		return newlists;*/
		
		//Create a  new LinkedHashSet
		
		Set<T> set = new LinkedHashSet<>();
		
		set.addAll(list);
		
		//clear the list
		list.clear();
		
		list.addAll(set);
		
		return list;
		
		
	}
	
	public static void main(String[] args) {
		
		int[] array = { 0, 12, 74, 26, 82, 3, 89, 8, 94, 3,89 };
		
		System.out.println("Duplicate elements in given array: ");  
        //Searches for duplicate element  
        for(int i = 0; i < array.length; i++) {  
            for(int j = i + 1; j < array.length; j++) {  
                if(array[i] == array[j])  
                    System.out.println(array[j]);  
            }  
        } 
		
		
		//get the ArrayList with duplicate values
		ArrayList<Integer> list = new ArrayList<>(Arrays.asList(1, 10, 1, 2, 2, 3, 3, 10, 3, 4, 5, 5));
		
		//Print the ArrayList
		System.out.println("ArrayList with Duplicate :: " +list);
		
		
		List<Integer> newList = list.stream().distinct().collect(Collectors.toList());
		
		System.out.println("ArrayList with duplicate removed :: " + newList);
		
		//Remove Duplicate
		ArrayList<Integer> dupReomveList  = removeDuplicates(list);
		
		//Print the ArrayList with Duplicated removed 
		System.out.println("ArrayList with duplicate removed set:: " + dupReomveList);

	}
	
	

	

}
