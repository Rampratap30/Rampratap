package com.program;

import java.util.Scanner;

public class Test {

	public static void main(String[] args) {
		/*
		 * HashMap<Integer, String> hashMap = new HashMap<Integer, String>();
		 * hashMap.put(12, "Test"); Collections.unmodifiableMap(hashMap);
		 * hashMap.put(13, "Test1"); System.out.println(hashMap);
		 */
		int sum = 0;
	      System.out.print("Enter the number value:: ");
	      Scanner sc = new Scanner(System.in);
	      int num = sc.nextInt();

	      for (int i = 0; i<num; i++){
	         sum = sum +i;
	      }
	      System.out.println("Sum of numbers : "+sum);

	}

}
