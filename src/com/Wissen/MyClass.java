package com.Wissen;

class A{
	public A() {
		System.out.println("A construct's::");
	}
	public void xyz() {
		System.out.println("A xyz ::");
	}
	
}

class B extends A{
	public B() {
		System.out.println("B construct's::");
	}
	public void xyz() {
		System.out.println("B xyz ::");
	}
}

public class MyClass {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		B b = new B();
		b.xyz();

	}

}
