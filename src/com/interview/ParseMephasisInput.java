package com.interview;

import java.util.*;
import java.util.stream.Collectors;

public class ParseMephasisInput {

	public static void main(String[] args) {
		
		String input = "Mobile 10000; car 800000; Bike 200000";
		Map<String, Integer> map = new HashMap<>();
		
		String[] items= input.split(";");
		for (String item : items) {
			String[] parts = item.trim().split(" ");
			if (parts.length == 2) {
				String name = parts[0];
				int price = Integer.parseInt(parts[1]);
				map.put(name, price);
			}
		}
		System.out.println(map);
		
		
		
		Map<String, Integer> itemPrices = Arrays.stream(input.split(";"))
	            .map(String::trim)
	            .map(s -> s.split(" "))
	            .collect(Collectors.toMap(
	                arr -> arr[0], arr -> Integer.parseInt(arr[1])
	            ));

	        // Output: {car=800000, Mobile=10000, Bike=200000}
	        System.out.println(itemPrices);


			/*---------------------------------------------------------------------------*/


		String s= "naga Balaji reddy";
		String[] sp = s.split(" ");
		System.out.println(sp[2]+" "+sp[1]+" "+sp[0]);

		int[] arr = {1,2,3,4,5,6};
		List<Integer> list = Arrays.stream(arr).boxed().collect(Collectors.toList());
		System.out.println(list);
		Collections.reverse(list);
		System.out.println(list);

		int n=arr.length;
		for(int i=n-1; i>=0; i--)
			System.out.print(arr[i]+" ");
	}

}
