package com.hash;

public class Employee {
	private int id;
	private String name;

	public Employee(int id, String name) {
		super();
		this.id = id;
		this.name = name;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	@Override
	public int hashCode() {
		
		int result = 1;
		final int prime = 31;
		result = prime * result + id;
		result = prime * result + ((name == null) ? 0 : name.hashCode());
		 

		return result;
	}

	@Override
	public boolean equals(Object obj) {

		
		Employee employee = (Employee) obj;
        if (employee.id == this.id) {
            employee.setName(this.name);
            return true;
        } else {
            return false;
        }
	}

}
