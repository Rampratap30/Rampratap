package com.comman;

/*an abstract class can contain constructors in Java. And a constructor of abstract class is called when an instance of a inherited class is created*/
abstract class Base {
	Base() {
		System.out.println("Base Class Constructor Called ::");
	}

	abstract void fun();
}

class Drived extends Base {

	Drived() {
		System.out.println("Drived Class Constructor Called ::");
	}

	@Override
	void fun() {
		System.out.println("Drived Fun() called");
	}
}

public class AbstractExamples {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		Drived d = new Drived();
		// d.fun();

		 Base b = new Drived();
		 b.fun();

	}

}
