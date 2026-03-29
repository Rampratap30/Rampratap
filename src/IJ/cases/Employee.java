package com.async.cases;

public class Employee {
    private String name;
    private String departments;
    private double salary;

    public Employee(String name, String departments, double salary) {
        this.name = name;
        this.departments = departments;
        this.salary = salary;
    }

    public String getName() {
        return name;
    }

    public String getDepartments() {
        return departments;
    }

    public double getSalary() {
        return salary;
    }

    @Override
    public String toString() {
        return "Employee{" +
                "name='" + name + '\'' +
                ", departments='" + departments + '\'' +
                ", salary=" + salary +
                '}';
    }
}
