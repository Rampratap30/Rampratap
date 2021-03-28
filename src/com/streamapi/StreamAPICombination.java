package com.streamapi;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class StreamAPICombination {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		List<String> list = Stream.of("Monkey", "Lion", "Giraffe","Lemur").filter(s-> s.startsWith("L")).map(String :: toUpperCase).collect(Collectors.toList());
		
		System.out.println(list);
		

		Stream<Character> chars = Stream.of("Monkey", "Lion", "Giraffe", "Lemur")
				.flatMap(s -> s.chars().mapToObj(i -> (char) i));

		System.out.println(chars.toString());

	}

}
