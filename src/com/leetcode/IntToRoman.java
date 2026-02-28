package com.leetcode;

import java.util.List;

public class IntToRoman {

	public static void main(String[] args) {
		int num = 500;
		List<String> cs = List.of("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I");
		List<Integer> vs = List.of(1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1);
		StringBuilder sb = new StringBuilder();
		for (int i = 0, n = cs.size(); i < n; i++) {
			while (num >= vs.get(i)) {
				sb.append(cs.get(i));
				num -= vs.get(i);
			}
			
		}
		System.out.println(sb.toString());		

	}

}
