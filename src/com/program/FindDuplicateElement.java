package com.program;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

public class FindDuplicateElement {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int[] duplicateFind = new int [] {111,222,3333,222,444,111};
		
		findDuplicatesUsingHashSet(duplicateFind);
		
		findDuplicatesUsingJava8(duplicateFind);

	}

	private static void findDuplicatesUsingJava8(int[] duplicateFind) {
		// TODO Auto-generated method stub
		Set<Integer> uniqueElements = new HashSet<>();
		Set<Integer> duplicateElements = Arrays.stream(duplicateFind).filter
				(i-> !uniqueElements.add(i)).boxed().collect(Collectors.toSet());
		System.out.println("Duplicate Element : ::: "+duplicateElements);
	}

	private static void findDuplicatesUsingHashSet(int[] duplicateFind) {
		// TODO Auto-generated method stub
		
		HashSet<Integer> set = new HashSet<Integer>();
		for(int element : duplicateFind) {
			if(! set.add(element))
			{
				System.out.println("Duplicate Element : "+element);
			}
		}
		
		
	}

}
