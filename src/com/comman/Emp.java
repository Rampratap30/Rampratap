package com.comman;

public class Emp {

	private String name;
	private String job;
	private int salary;

	public Emp(String name, String job, int salary) {
		super();
		this.name = name;
		this.job = job;
		this.salary = salary;
	}

	public void display() {
		System.out.println(this.name + "\t" + this.job + "\t" + this.salary);
	}

	public boolean equals(Object paramObject) {
		Emp localEmp = (Emp) paramObject;
		return (this.name.equals(localEmp.name)) && (this.job.equals(localEmp.job)) && (this.salary == localEmp.salary);
	}

	public int hashCode() {
		return this.name.hashCode() + this.job.hashCode() + this.salary;
	}

	public int compareTo(Object paramObject) {
		Emp localEmp = (Emp) paramObject;
		return this.name.compareTo(localEmp.name);
	}

}
