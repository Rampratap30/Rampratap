package com.hackerrank;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.Scanner;

public class DuplicateCointPair {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		/*
		 * int[] arr = {1,4,7,1,7,4,1,5}; Map<Integer, Integer> counts = new
		 * HashMap<Integer,Integer>(); int count = 0;
		 * 
		 * for(Integer num:arr){ Integer entry = counts.get(num);
		 * 
		 * if(entry == null){ counts.put(num, 1); }else if(counts.get(num) == 1){
		 * count++; counts.put(num, counts.get(num) + 1); } }
		 * 
		 * System.out.println(count);
		 */
	    
		/*
		 * int[] arr = {1,1,1,1,1,1,4,7,1,7,4,1,5}; HashMap<Integer,Integer> asd = new
		 * HashMap<Integer, Integer>(); for(int i=0;i<arr.length;i++) {
		 * if(asd.get(arr[i]) == null) { asd.put(arr[i], 1); } else { asd.put(arr[i],
		 * asd.get(arr[i])+1); } }
		 * 
		 * //print out for(int key:asd.keySet()) { //get pair int temp = asd.get(key)/2;
		 * if(temp > 0) { System.out.println(key+" have : "+temp+" pair"); } }
		 */
		
		Scanner in = new Scanner(System.in);

		int t = in.nextInt();
		int[] ar = new int[t];
		for (int i = 0; i < t; i++) {

			int a = in.nextInt();
			ar[i] = a;
		}
		int count = solved(t, ar);
		System.out.println("Count :: " + count);
		 
		

	}

	private static int solved(int t, int[] ar) {
		
		Arrays.sort(ar);		
		int count = 0;
		
		for(int i =0; i < t-1;i++) {
			if(ar[i]==ar[i+1]) {
				count++;
				i++;
			}
		}
		/*
		 * for(int i =0 ;i < ar.length; i++) { for(int j =i+1 ;j < ar.length; j++) {
		 * if(ar[i]==ar[j]) { System.out.println(ar[j]); count++; } } }
		 */
		
		
		return count;
		/*
		 *9
		 10 20 20 10 10 30 50 10 20 
		 */
	}

}
