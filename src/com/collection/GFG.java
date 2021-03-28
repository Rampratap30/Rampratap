package com.collection;

import java.util.HashMap;
import java.util.Map;

public class GFG {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		Geek g1 = new Geek("A", 1);
		Geek g2 = new Geek("A", 1);

		Map<Geek, String> map = new HashMap<Geek, String>();

		map.put(g1, "CSE");
		map.put(g2, "IT");

		System.out.println("Size :: "+ map.size());
		for (Geek geek : map.keySet()) {
			System.out.println(map.get(geek).toString());
		}
		 
		
		/*
		 * Geek gg = null; gg.sound();
		 */
	}

}
