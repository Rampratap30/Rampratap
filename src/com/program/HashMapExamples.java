package com.program;

import java.util.HashMap;
import java.util.Map.Entry;

public class HashMapExamples {
	
	String color;
	HashMapExamples(String c){
		color = c;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((color == null) ? 0 : color.hashCode());
		return result;
	}



	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		HashMapExamples other = (HashMapExamples) obj;
		if (color == null) {
			if (other.color != null)
				return false;
		} else if (!color.equals(other.color))
			return false;
		return true;
	}



	@Override
	public String toString() {
		return "HashMapExamples [color=" + color + "]";
	}


	public static void main(String[] args) {
		// TODO Auto-generated method stub		
		HashMapExamples d1 = new HashMapExamples("red");
		HashMapExamples d2 = new HashMapExamples("black");
		HashMapExamples d3 = new HashMapExamples("white");
		HashMapExamples d4 = new HashMapExamples("white");
		HashMap<HashMapExamples, Integer> hashMap = new HashMap<HashMapExamples, Integer>();
		
		//TreeMap<HashMapExamples, Integer> hashMap = new TreeMap<HashMapExamples, Integer>();
		
		hashMap.put(d1, 10);
		hashMap.put(d2, 15);
		hashMap.put(d3, 5);
		hashMap.put(d4, 20);
		
		System.out.println(hashMap.size());
		
		for(Entry<HashMapExamples, Integer> entry : hashMap.entrySet()) {
			System.out.println(entry.getKey().toString()+" - " + entry.getValue());
		}
 

	}

}
