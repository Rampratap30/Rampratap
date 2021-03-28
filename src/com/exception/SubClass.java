package com.exception;

//Case 1: If SuperClass doesn’t declare any exception and subclass declare checked exception 
public class SubClass extends SuperClass{
	
	void method() throws ArithmeticException {
		System.out.println("Sub Class ::");
	}

	public static void main(String[] args) {
		SuperClass sub = new SubClass();
		sub.method();

	}

}

class SuperClass{
	void method() {
		System.out.println("Super Class ::");
	}
}
