package com.collection;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

public class Fail_Safe {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		/*
		 * ConcurrentHashMap<String,Integer> chm = new ConcurrentHashMap<String,
		 * Integer>();
		 * 
		 * chm.put("Dell", 1); chm.put("Sony", 2);
		 * 
		 * //Getting an Iterator from map Iterator<String> itr =
		 * chm.keySet().iterator();
		 * 
		 * while(itr.hasNext()){ String key = (String)itr.next();
		 * 
		 * System.out.println(key+" " + chm.get(key)); chm.put("Lenovo", 3); }
		 */
		
		
		Integer[] a = {3, 2, 1, 1, 2};
		List<Integer> l = new LinkedList<Integer>();
		for(Integer i: a) {
		    if (!l.contains(i)) {
		        l.add(i);
		    }
		}
		for(Integer j: l) {
		    //System.out.print(" " + j);
		}
		
		Integer[] aa = {30000, 20000, 10000, 10000, 20000};
		Map<String,Integer> ll = new HashMap<String,Integer>();
		for(int i=0; i<aa.length; i++) {
		    ll.put("intVal:" + aa[i], i);
		}
		for(String e: ll.keySet()) {
		    //System.out.print(" " + ll.get(e));
		}
		
		
		Integer[] a1 = {3, 2, 10000, 10000, 2};
		Set<Integer> l1 = new TreeSet<Integer>();
		for(Integer i: a1) {
		    l1.add(i);
		}
		for(Integer j: l1) {
		    //System.out.print(" " + j);
		}
		
		Integer[] a2 = {3, 2, 10000, 10000, 2};
		Set<Integer> l2 = new HashSet<Integer>();//ore
		for(Integer i: a2) {
		    l2.add(i);
		}
		for(Integer j: l2) {
		    System.out.print(" " + j);
		}
		
	}

}
