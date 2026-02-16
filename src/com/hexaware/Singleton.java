package com.hexaware;

public class Singleton {
	
	// Static variable reference of single_instance
    // of type Singleton
	private static Singleton instance= null;
	
	public String str;
	
	// Private constructor restricted to this class itself
	
	private Singleton() {
		str = "Hello I am a string part of Singleton class";
	}
	
	// Static method to create instance of Singleton class
	
	public static Singleton getInstance() {
		if (instance == null) {
			instance = new Singleton();
		}
		return instance;
	}
}
