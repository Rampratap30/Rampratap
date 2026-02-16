package com.hexaware;


import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ConvertMapToList {

	public static void main(String[] args) {
	
		Map<Integer, String> map = new HashMap<>();
		map.put(30,"Alice");
		map.put(25,"Bob");
		map.put(35,"Charlie");
		
		List<Map.Entry<Integer, String>> list = map.entrySet().stream().collect(Collectors.toList());
		
		System.out.println("List of Map Entries:"+list);
		

	}

}
