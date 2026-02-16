package com.hexaware;

public class FactorialForLoop {

	public static void main(String[] args) {
	
		int number = 5; // Change this to calculate factorial of a different number
		long factorial = 1;

		for (int i = 1; i <= number; i++) {
			factorial *= i; // factorial = factorial * i
		}

		System.out.println("Factorial of " + number + " is: " + factorial);

	}

}
