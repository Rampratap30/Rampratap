package com.program;

import java.util.HashMap;

public class Employee {
	
	String name;
	int empId;
	
	
	public Employee(int empId, String name) {
		this.empId=empId;
		this.name = name;
	}
	
	@Override
	public int hashCode() {
		//System.out.println("Calling hascode method of employee");		
		/*String str = this.name;
		Integer sum  = 0;		
		 for(int i=0;i<str.length();i++){
			 sum = sum+str.charAt(i);
		 }	*/	
		return empId;
	}
	
	public boolean equals(Object obj) {
		
		//System.out.println("calling equals method of Employee");
	    Employee emp=(Employee)obj;
	    
	    if(this.empId == emp.empId) {
	    	
	    	//System.out.println("returning true");
	        return true;
	    }else{
	        //System.out.println("returning false");
	        return false;
	    }
		
	}
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Employee emp1 = new Employee(1, "Ram");
		Employee emp2 = new Employee(2, "Ram");
		
		HashMap<Employee, Employee> map = new HashMap<>();
		map.put(emp1, emp1);
		map.put(emp2, emp2);
		
		
		System.out.println("size of hashmap ::" + map.size());
		
		System.out.println(emp1.hashCode());
        System.out.println(emp2.hashCode());
        System.out.println(emp1.equals(emp2));
	}

}
