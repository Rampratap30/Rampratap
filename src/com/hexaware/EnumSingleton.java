package com.hexaware;

public enum EnumSingleton {
	INSTANCE;

	public void showMessage() {
		System.out.println("Doing something for Singleton instance...");
	}
}
