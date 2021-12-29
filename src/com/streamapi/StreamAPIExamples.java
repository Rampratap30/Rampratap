package com.streamapi;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class StreamAPIExamples {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		List<String> userList = new ArrayList<String>();
		userList.add("Ram");
		userList.add("Sohita");
		userList.add("Aadya");
		userList.add("Aadvik");
		
		userList.stream().filter(s->s.startsWith("A")).forEach(System.out::println);
		System.out.println("-------------------------------");
		String firstMatchName = userList.stream().filter(s->s.startsWith("S")).findFirst().get();
		System.out.println(firstMatchName);
		System.out.println("-------------------------------");
		List<String> members = userList.stream().sorted().map(String :: toUpperCase).collect(Collectors.toList());
		
		System.out.println(members);

	}

}
