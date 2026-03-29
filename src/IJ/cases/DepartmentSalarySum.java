package com.async.cases;


import java.util.*;
import java.util.stream.Collectors;

public class DepartmentSalarySum {

    public static void main(String[] args) {
        List<Employee> employees = Arrays.asList(
                new Employee("Alice", "HR", 50000.0),
                new Employee("Bob", "IT", 70000.0),
                new Employee("Charlie", "HR", 45000.0),
                new Employee("David", "IT", 80000.0),
                new Employee("Frank", "IT", 65000.0),
                new Employee("Eve", "Sales", 60000.0)

        );

        // Compute sum of salaries by department
        Map<String, Double> mapResults = employees.stream().
                collect(Collectors.groupingBy(
                        Employee::getDepartments,
                        Collectors.summingDouble(Employee::getSalary)
                ));

        System.out.println("Total Salaries by Departments");
        mapResults.forEach((department, totalSalary)->
                System.out.println(department+" "+totalSalary));

        System.out.println("---------------------------------------");

        List<String> getEmployees =  employees.stream().map(Employee::getName).collect(Collectors.toList());
        System.out.println("Employee name is ::"+getEmployees);
        System.out.println("---------------------------------------");

        // Accumulate names into a TreeSet
        Set<String> set = employees.stream()
                .map(Employee::getName)
                .collect(Collectors.toCollection(TreeSet::new));

        System.out.println("Set ::--->"+set);
        System.out.println("---------------------------------------");

        // Compute sum of salaries of employee
        Double total = employees.stream()
                .collect(Collectors.summingDouble(Employee::getSalary));

        System.out.println("Total Salary ::--->"+total);


        // Group employees by department  Map<Department, List<Employee>> byDept = employees.stream()    .collect(Collectors.groupingBy(Employee::getDepartment));
    }
}

