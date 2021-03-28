package com.program;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class SetNULL {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		HashSet<String> hs = new HashSet<String>();
		
		hs.add(null);
		hs.add(null);
		hs.add("Infinx");
		
		System.out.println("Display Hashset :: " + hs);
		
		List<String> list = new ArrayList<String>();
		list.add("Ram");
		list.add("Pratap");
		
		System.out.println("list diplay ::" +list);
		
		list.remove("Pratap");
		list.remove("Ram");
		list.add(null);
		System.out.println("after remove list diplay ::" +list);
		

	}

}
