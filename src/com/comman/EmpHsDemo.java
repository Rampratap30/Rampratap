package com.comman;

import java.util.HashSet;
import java.util.Iterator;

public class EmpHsDemo {

	public static void main(String[] args) {
	    HashSet localHashSet = new HashSet();
	    localHashSet.add(new Emp("Ram", "Trainer", 34000));
	    localHashSet.add(new Emp("Ravi", "Administrator", 44000));
	    localHashSet.add(new Emp("Sachin", "Programmer", 24000));
	    localHashSet.add(new Emp("Priyanka", "Manager", 54000));
	    localHashSet.add(new Emp("Anupam", "Programmer", 34000));
	    localHashSet.add(new Emp("Sachin", "Team Leader", 54000));
	    System.out.println("There are " + localHashSet.size() + " elements in the set.");
	    System.out.println("Content of set are : ");
	    Iterator localIterator = localHashSet.iterator();
	    while (localIterator.hasNext())
	    {
	      Emp localEmp1 = (Emp)localIterator.next();
	      System.out.print(localEmp1.hashCode() + "\t");
	      localEmp1.display();
	    }
	    Emp localEmp1 = new Emp("Ravi", "Administrator", 44000);
	    System.out.println("Removing following Emp from the set...");
	    System.out.print(localEmp1.hashCode() + "\t");
	    localEmp1.display();
	    localHashSet.remove(localEmp1);
	    System.out.println("No. of elements after removal " + localHashSet.size());
	    Emp localEmp2 = new Emp("Anupam", "Programmer", 34000);
	    System.out.println("Searching following Emp in the set...");
	    System.out.print(localEmp2.hashCode() + "\t");
	    localEmp2.display();
	    System.out.println("Results of searching is : " + localHashSet.contains(localEmp2));

	}

}
