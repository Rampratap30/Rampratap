package com.hackerrank;

import java.util.stream.Collectors;
import java.util.stream.Stream;

public class StringExamples {

	public static void main(String[] args) {
		String test="example";
		  System.out.println(Stream.of(test.split("")).collect(Collectors.joining(", ")));

	}

}
