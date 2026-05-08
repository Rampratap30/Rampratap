package com.employee;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

//==== https://medium.com/@veenaraofr/java8-stream-api-commonly-asked-questions-about-employee-highest-salary-99c21cec4d98

public class SecondHighestSalary {
    public static void main(String[] args) {
        List<Employee> employeesList = List.of(
                new Employee("Rampratap",95000),
                new Employee("Sohita",85000),
                new Employee("Aadya",98000),
                new Employee("Aadvik",90000)
        );

        Optional<Employee> results = employeesList.stream().sorted(Comparator.comparingDouble(Employee::getSalary).reversed()).skip(1).findFirst();

        System.out.println("Second Highest Salary ::"+ results.get().getSalary());


        Optional<Employee> highestSalary = employeesList.stream().sorted(Comparator.comparingDouble(Employee::getSalary).reversed()).findFirst();

        System.out.println("Highest Salary ::"+highestSalary.get().getSalary());
    }
}
