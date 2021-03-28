package com.Synechron;

public class Employee {

	private String name;
	private int age;

	public Employee(int age, String name) {
		this.age = age;
		this.name = name;
	}

	// Getters and Setters of name & age go here
	public String toString() {
		return  "Age:" + this.age+" || Employee Name:" + this.name;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Integer getAge() {
		return age;
	}

	public void setAge(Integer age) {
		this.age = age;
	}
}
