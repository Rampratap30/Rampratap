package com.hackerrank;

import java.util.ArrayList;
import java.util.List;

public class Solution_8 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		List<Integer> a = new ArrayList<Integer>();
		a.add(17);
		a.add(28);
		a.add(30);
		
		List<Integer> b = new ArrayList<Integer>();
		b.add(99);
		b.add(16);
		b.add(8);
		
		int al = 0, bo = 0;
		if(a.get(0) > b.get(0)) {
				al++;
		}
		if(b.get(0) > a.get(0)) {
			bo++;
		}
		if(a.get(1) > b.get(1)) {
			al++;
		}
		if(b.get(1) > a.get(1)) {
			bo++;
		}
		if(a.get(2) > b.get(2)) {
			al++;
		}
		if(b.get(2) > a.get(2)) {
			bo++;
		}
		
		System.out.println(al+" "+bo);
		
		 

	}

}
