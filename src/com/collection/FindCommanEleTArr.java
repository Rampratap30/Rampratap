package com.collection;

import java.util.ArrayList;
import java.util.stream.Collectors;

public class FindCommanEleTArr {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		ArrayList<String> list = new ArrayList<>();
		
		list.add("A");
		list.add("B");
		list.add("C");
		list.add("D");
		list.add("E");
		list.add("F");

		System.out.println("List :: " +list);
		
		ArrayList<String> list1 = new ArrayList<>();
		
		list1.add("E");
		list1.add("F");
		list1.add("G");
		list1.add("H");
		list1.add("A");
		list1.add("C");
		
		System.out.println("List1 :: " + list1);
		
		//list.retainAll(list1);
		
		System.out.println(list.stream().filter(list1 :: contains).collect(Collectors.toList()));
		
		//System.out.println("Comman Elements :: " + list);
		
		
		
		
		
	}

}
