package com.hackerearth;

import java.util.Scanner;

public class DisplayIndiviChar {

	public static void main(String[] args) {

		Scanner sc = new Scanner(System.in);
		System.out.println("Enter any String:");
		String name = sc.nextLine();
		System.out.println("Before Splited: " + name);

		String[] sname = name.split("");
		String joined1 = String.join(",", sname);
		joined1 = joined1.replace(" ,", " ").replace(", ", " ");
		System.out.println(joined1);

		
		/*
		 * for (int i = 0; i < name.length(); i++) {
		 * 
		 * System.out.println(name.charAt(i) + ",");
		 * 
		 * if (i > 0 || i <= name.length()) { System.out.println(name.charAt(i));
		 * System.out.println(","); }
		 * 
		 * 
		 * if((i+1) < name.length() && !name.charAt(i+1).equals(" ")) {
		 * 
		 * }
		 * 
		 * }
		 */
		sc.close();

		/*
		 * String str = "Java language";
		 * System.out.println(Stream.of(str.split("")).collect(Collectors.joining(", "))
		 * );
		 */

	}

}
