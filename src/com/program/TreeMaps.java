package com.program;

import java.util.Map.Entry;
import java.util.TreeMap;

class Dog implements Comparable<Dog>{
	
	String color;
	int size;
	Dog(String c, int s){
		color = c;
		size = s;
	}

	@Override
	public String toString() {
		return "Dog [color=" + color + ", size=" + size + "]";
	}

	@Override
	public int compareTo(Dog o) {
		// TODO Auto-generated method stub
		return o.size - this.size;
	}
	
}

public class TreeMaps {

	public static void main(String[] args) {
		Dog d1 = new Dog("red", 30);
		Dog d2 = new Dog("black", 20);
		Dog d3 = new Dog("white", 40);
		Dog d4 = new Dog("white", 10);
		
		TreeMap<Dog, Integer> treeMap = new TreeMap<Dog, Integer>();
		
		treeMap.put(d1, 10);
		treeMap.put(d2, 15);
		treeMap.put(d3, 5);
		treeMap.put(d4, 20);
		
		System.out.println(treeMap.size());
		
		for (Entry<Dog, Integer> entry : treeMap.entrySet()) {
			System.out.println(entry.getKey() + " - " + entry.getValue());
		}

	}

}
