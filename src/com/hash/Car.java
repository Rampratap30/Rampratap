package com.hash;

import java.util.HashMap;

public class Car {
	
	 private String color;

	    public Car(String color) {
	        this.color = color;
	    }
	    
	    public int hashCode(){  
	    	  return this.color.hashCode(); 
	    	}

	    public boolean equals(Object obj) {
	        if(obj==null) return false;
	        if (!(obj instanceof Car))
	            return false;   
	        if (obj == this)
	            return true;
	        return this.color.equals(((Car) obj).color);
	    }

	    public static void main(String[] args) {
	        Car a1 = new Car("green");
	        Car a2 = new Car("red");

	        //hashMap stores Car type and its quantity
	        HashMap<Car, Integer> m = new HashMap<Car, Integer>();
	        m.put(a1, 10);
	        m.put(a2, 20);
	        System.out.println(m.get(new Car("green")));
	    }
	    
	    /*The problem is caused by the un-overridden method hashCode(). The contract between equals() and hashCode() is:

	    	If two objects are equal, then they must have the same hash code.
	    	If two objects have the same hash code, they may or may not be equal.

	    	public int hashCode(){  
	    	  return this.color.hashCode(); 
	    	}*/

}
