 package com.hackerrank;

public class ElectricityBill {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int units = 250;
		
		System.out.println(calculateBill(units));

	}

	private static int calculateBill(int units) {
		// TODO Auto-generated method stub
		
		if(units <=100) {
			return units * 10;
		}else if(units <=200) {
			return (100 * 10)+(units-100)*15;
		}else if(units <=300) {
			return (100 * 10)+(100 * 15)+(units-200)*20;
		}else if(units > 300) {
			return (100 * 10)+(100 * 15)+(100 * 20)+(units-300)*25;
		}
		
		
		return 0;
	}

}
