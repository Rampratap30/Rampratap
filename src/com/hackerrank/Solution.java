package com.hackerrank;

import java.util.Scanner;

public class Solution {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		/*Scanner scan = new Scanner(System.in);

		int i = Integer.parseInt(scan.nextLine());
		double d = Double.parseDouble(scan.nextLine());
		String s = scan.nextLine();*/
		

		

		/*
		 * String s = "Welcome to HackerRank's Java tutorials!";
		 * 
		 * double d = 3.1415;
		 * 
		 * int i = 42;
		 */
		// Write your code here.

		/*System.out.println("String: " + s);
		System.out.println("Double: " + d);
		System.out.println("Int: " + i);*/



		int sum = 0;
		for (int i = 1; i < 200; i++) {
			if (i % 3 == 0 || i % 5 == 0) sum += i;
		}
		System.out.print(sum);

	}

}
