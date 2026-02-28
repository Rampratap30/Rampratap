package com.leetcode;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class CountRepeatChar {

	public static void main(String[] args) {
		
		String inputString ="Rampratap";
		
		Map<Character, Long> resultCount = inputString.toLowerCase().chars().
				mapToObj(c->(char)c).filter(c-> !Character.isWhitespace(c)).
				collect(Collectors.groupingBy(c->c,Collectors.counting()));
		
		System.out.println(resultCount);
		
		
		List<String> list = Arrays.asList("Rampratap","Raja","Rani","Rajveer");
		
		Map<String, Integer> resultCountAs = list.stream().collect(Collectors.toMap(s->s,String::length));
		System.out.println(resultCountAs);
		
		
		
				

	}

}
