package com.Synechron;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class StreamFliterEx {
	static List<Employee> employeeList = Arrays.asList(new Employee(45,"Tom Jones"),
		      new Employee(26,"Harry Major"),
		      new Employee(65,"Ethan Hardy"),
		      new Employee(22,"Nancy Smith"),
		      new Employee(21,"Catherine Jones"));
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Comparator<Employee> compare = Comparator.comparing(Employee :: getName);
		List<Employee> list = employeeList.stream().filter(emp->emp.getAge() == 26).sorted(compare).collect(Collectors.toList());
		
		System.out.println(list);

	}

}
