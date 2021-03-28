package com.hash;

import java.util.HashSet;

public class HashingExample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		Employee emp1 = new Employee(1, "Ram");
		Employee emp2 = new Employee(1, "Sohita");
		Employee emp3 = new Employee(1, "Aadya");
		Employee emp4 = new Employee(4, "Aadvik");
		
		HashSet<Employee> sset=new HashSet<Employee>();

		//TreeSet<Employee> sset=new TreeSet<Employee>();//cannot be cast to java.lang.Comparable
		
		sset.add(emp1);
		sset.add(emp2);
		sset.add(emp3);
		sset.add(emp4);
		
		System.out.println("HashSet size ::"+sset.size());
		
		for (Employee emp : sset) {
			System.out.println(emp.getId() +" "+emp.getName() +" HASHCODE :: "  +emp.hashCode());
		}
		
		

	}

}
