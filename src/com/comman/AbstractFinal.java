package com.comman;


abstract class Base1{
	
	final int ii = 100;
	
	final void fun() {
		
		
		System.out.println("Base-1 Class ::" +100);
	}
	
}
class Drived1 extends Base1{
	
	/*
	 * void fun() { System.out.println("Base-1 Class ::" +100); }
	 */
	
}

public class AbstractFinal {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		Base1 b = new Drived1();
		b.fun();

	}

}
