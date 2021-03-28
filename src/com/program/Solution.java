package com.program;

import java.util.Scanner;

public class Solution {

	public static void main(String[] args) {
		/*Scanner scan = new Scanner(System.in);
		System.out.print("Enter i ::");
        int i = scan.nextInt();
        System.out.print("Enter d ::");
        double d = scan.nextDouble();        
        System.out.print("Enter s ::");*/
        Scanner scans = new Scanner(System.in);
        System.out.print("Enter s ::");
        String token = null;
        while(scans.hasNextLine()) {
        	token  = scans.nextLine();       	
        }
        System.out.println("String: " + token);
        /*System.out.print("Enter s ::");
        String s = scans.next();*/
        
        //System.out.println("String: " + s.length());

        // Write your code here.

        /*System.out.println("String: " + s);
        System.out.println("Double: " + d);
        System.out.println("Int: " + i);*/

	}

}
