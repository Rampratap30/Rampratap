package com.hexaware;

public class Singleton_Example {

	public static void main(String[] args) {
		EnumSingleton singletonInstance = EnumSingleton.INSTANCE;
		EnumSingleton anotherInstance = EnumSingleton.INSTANCE;
		
		if (singletonInstance == anotherInstance) {
			System.out.println("Both instances are the same. Singleton works!");
		} else {
			System.out.println("Instances are different. Singleton failed.");
		}

	}

}
