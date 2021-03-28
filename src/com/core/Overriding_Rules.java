/**
 * 
 */
package com.core;

/**
 * @author rampr
 *
 */

class Super{
	void show() {
		System.out.println("Super Class ::");
	}
}
public class Overriding_Rules extends Super  {

	void show() //throws IOException // Compile time error- Checked Exception
	{
		System.out.println("parent class");
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		{
		    Super s=new Overriding_Rules();
		    s.show();
		  }

	}
	/*
	 * the method show() doesn't throw any exception when its declared/defined in the Super class, hence its overridden version in the class Sub also cannot throw any checked exception.
	 * 
	 */

}
