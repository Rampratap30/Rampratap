package com.collection;

import java.util.AbstractSet;
import java.util.HashMap;
import java.util.Iterator;

public class CustomHashSetTest extends AbstractSet{
	
	private HashMap<Object,Object> map = null;
	
	private static final Object tempObject = new Object();
	
	public CustomHashSetTest() {
		map= new HashMap();
	}
	
	public boolean add(Object object) {
		return map.put(object, tempObject)==null;
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		CustomHashSetTest test = new CustomHashSetTest();
		
		test.add("Ram");
		test.add("Sohita");
		test.add("Aadya");
		test.add("Aadvik");
		test.add("Ram");
		
		for (Object object : test) {
			System.out.println(object.toString());
		}
		

	}

	@Override
	public Iterator iterator() {
		// TODO Auto-generated method stub
		return map.keySet().iterator();
	}

	@Override
	public int size() {
		// TODO Auto-generated method stub
		return map.size();
	}

}
