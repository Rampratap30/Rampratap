package com.Wissen;

class A1{
	public void xyz() {
		System.out.println("A1 :: ");
	}
}

class B1 extends A1{
	public void xyz() {
		System.out.println("B1 :: ");
	}
}

public class MyClass1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		//B1 b = new A1();
		
		A1 aa = new B1();
		aa.xyz();

	}

}
