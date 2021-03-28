package com.program;

import java.util.Scanner;

public class LinearSearchExample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int counter,item,num,array[];
		
		Scanner input = new Scanner(System.in);
		System.out.println("Enter number of elements ::");
		num = input.nextInt();
		
		array = new int[num];
		
		System.out.println("Enter " +num+"integers");
		
		for(counter=0; counter<num;counter++)
			array[counter] = input.nextInt();
		System.out.println("Enter the search value:");
		
		item = input.nextInt();
		for(counter=0; counter<num;counter++)
		{
			if(array[counter]==item) {
				System.out.println(item +" is present at location " + (counter+1));
				break;
			}
		}
	}

}
