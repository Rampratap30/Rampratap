package com.streamapi;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class StreamAPISorting {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		ArrayList<Employee> employees = getUnsortedEmployeeList();
		
		Comparator<Employee> compare = Comparator.comparing(Employee :: getFirstName).thenComparing(Employee :: getLastName);
		
		List<Employee> sortedEmployees = employees.stream().sorted(compare).collect(Collectors.toList());
		
		sortedEmployees.forEach(System.out :: println);

	}
	
	private static ArrayList<Employee> getUnsortedEmployeeList() {
		ArrayList<Employee> list = new ArrayList<>();
        list.add( new Employee(2l, "Lokesh", "Gupta") );
        list.add( new Employee(1l, "Alex", "Gussin") );
        list.add( new Employee(4l, "Brian", "Sux") );
        list.add( new Employee(5l, "Neon", "Piper") );
        list.add( new Employee(3l, "David", "Beckham") );
        list.add( new Employee(7l, "Alex", "Beckham") );
        list.add( new Employee(6l, "Brian", "Suxena") );
        return list;
	}

	static class Employee {

		private long id;
        private String firstName;
        private String lastName;

        public Employee(long id, String firstName, String lastName) {
        	this.id = id;
            this.firstName = firstName;
            this.lastName = lastName;
        }

        public String getFirstName() {
            return firstName;
        }

        public void setFirstName(String firstName) {
            this.firstName = firstName;
        }
        
        public String getLastName() {
            return lastName;
        }

        public void setLastName(String lastName) {
            this.lastName = lastName;
        }

        public long getId() {
            return id;
        }

        public void setId(long id) {
            this.id = id;
        }

        @Override
        public String toString() {
            return "Employee{" +
                    "FirstName='" + firstName + '\'' +
                    ", id=" + id+
                    '}';
        }
	}

}
