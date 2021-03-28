package com.collection;


import java.util.HashMap;
import java.util.Iterator;

public class Fail_Fast {
	
	public void myBuf (StringBuffer s, StringBuffer s1) {
        s.append ("B");
        s = s1;
    }
	
	protected static void swap (int a, int b) {
		int temp = a;
		a=b;
		b=temp;
	}

	public static void main(String[] args) {
		
		
		int a =10,B=20;
		/*
		 * int ii = 15;
		 * 
		 * if(ii>10) if(ii>20) System.out.println("A"); else System.out.println("B");
		 */
		Integer aa =null;
		int b = aa;
		System.out.println(b);
				
		
		Fail_Fast t = new Fail_Fast();
        StringBuffer s = new StringBuffer ("A");
        StringBuffer sl = new StringBuffer ("B");
        t.myBuf(s, sl);
        System.out.print(s);
				
		
		// TODO Auto-generated method stub
		
		/*
		 * List<String> list = new ArrayList<String>(); list.add("A"); list.add("B");
		 * list.add("C"); Iterator<String> itr = list.iterator(); while(itr.hasNext()) {
		 * String str = (String)itr.next(); System.out.println(str); list.add("D"); }
		 */
		
		/*
		 * HashMap<String,Integer> hm = new HashMap<String,Integer>(); hm.put("A", 1);
		 * hm.put("B", 2); hm.put("C", 3);
		 * 
		 * Iterator<String> itrs = hm.keySet().iterator(); while(itrs.hasNext()) {
		 * String key = (String) itrs.next(); System.out.println(key + " "
		 * +hm.get(key)); hm.put("D", 4); }
		 */
		
	}

}
