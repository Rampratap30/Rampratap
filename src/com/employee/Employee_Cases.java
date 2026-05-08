package com.employee;

import java.util.*;
import java.util.stream.Collectors;

public class Employee_Cases {
    public static void main(String[] args) {

        List<Employee> employees = Arrays.asList(
                new Employee(1, "John", "Doe", 30, "IT", 60000, 2015, "New York", "Male"),
                new Employee(2, "Alice", "Smith", 28, "HR", 55000, 2017, "Los Angeles", "Female"),
                new Employee(3, "Mike", "Johnson", 35, "Finance", 70000, 2010, "Chicago", "Male"),
                new Employee(4, "Ishan", "Kishan", 26, "IT", 80000, 2022, "Bihar India", "Male"),
                new Employee(4, "prithvi", "Shaw", 28, "Product Development", 90000, 2022, "Bihar India", "Male"),
                new Employee(4, "Aaksh", "Deep", 25, "Product Development", 70000, 2021, "Delhi India", "Male"),
                new Employee(1, "sehwag", "Doe", 38, "IT", 90000, 2012, "Noida India", "Male"),
                new Employee(1, "Ankita", "kohali", 38, "IT", 92000, 2011, "Gurugram India", "Female")
        );

        // 1) Filter the list of employees who are from the IT department.
        List<Employee> empFromITDepartment = employees.stream()
                .filter(e->e.getDepartment().equalsIgnoreCase("IT"))
                .collect(Collectors.toList());

        //System.out.println("Employees who are from the IT department "+empFromITDepartment);

        // Print the details of IT department employees
        //empFromITDepartment.forEach(System.out::println);

        //Calculate the average salary of IT department employees
        double averageSalOfITEmp = employees.stream().mapToDouble(Employee::getSalary).average().orElse(0.0);
        //System.out.println("average salary of IT department employees "+averageSalOfITEmp);

//        double avgSalary = employees.stream()
//                .filter(e -> e.getDepartment().equals("IT"))
//                .peek(System.out::println)
//                .collect(Collectors.averagingDouble(Employee::getSalary));
        //System.out.println("Average Salary: " + avgSalary);

        //------------------OR---------------
//        OptionalDouble avgSalary = employees.stream()
//                .filter(e -> e.getDepartment().equals("IT"))
//                .peek(System.out::println)
//                .mapToDouble(Employee::getSalary)
//                .average();

        //System.out.println("Average Salary: " + avgSalary.orElse(0.0));

        //Print the details of the top 3 highest-paid employees who are from the IT department and have a salary greater than 60000.

        List<Employee> empSalGreater = employees.stream()
                .filter(e->e.getDepartment().equalsIgnoreCase("it") && e.getSalary() > 60000)
                .limit(3)
                .sorted(Comparator.comparingDouble(Employee::getSalary).reversed())
                .collect(Collectors.toList());

        //empSalGreater.forEach(System.out::println);
        //System.out.print(empSalGreater);

        //List down the names of all employees in each department

        Map<String, List<String>> empDepartment = employees.stream()
                .collect(Collectors.groupingBy(Employee::getDepartment,Collectors.mapping(Employee::getFirstName,Collectors.toList())));

//        empDepartment.forEach((department,name)->{
//                    System.out.println("-----------------------");
//                    System.out.println(department + name);
//                }
//            );


        //— — — — — Another way — — — — — —

        Map<String, List<Employee>> empListByDepart =
                employees.stream().collect(
                        Collectors.groupingBy(Employee::getDepartment));


//        empListByDepart.forEach((department, employeess)->{
//            System.out.println("----------------------------------------");
//            System.out.println("Employees in " + department + " : ");
//            System.out.println("----------------------------------------");
//            employeess.forEach(emp-> System.out.println(emp.getFirstName()+emp.getLastName()));
//        });

        Map<String,List<Employee>> cityByEmployeeList = employees.stream()
                .collect(Collectors.groupingBy(Employee::getCity));

        cityByEmployeeList.forEach((city, employeess)->{
            System.out.println("----------------------------------------");
            System.out.println("Employee in "+city+" : ");
            System.out.println("----------------------------------------");
            employeess.forEach(emp-> System.out.println(emp.getFirstName()+ emp.getLastName()));
        });

        System.out.println("-------------------------------------------------------------------------------------------------");

        //Calculate the total salary of employees in the IT department
        double totalSalary  = employees.stream()
                .filter(e->e.getDepartment().equalsIgnoreCase("IT"))
                .mapToDouble(Employee::getSalary)
                .sum();
        //System.out.println("Total Salary for IT Department: " + totalSalary);

        //Find the employee with the highest salary in the IT department?

        Optional<Employee> highestPaid = employees.stream()
                .filter(e -> e.getDepartment().equals("IT"))
                .max(Comparator.comparingDouble(Employee::getSalary));
        highestPaid.ifPresent(System.out::println);

        //System.out.println("-------------------------------------------------------------------------------------------------");
        //Group employees by department and print the count of employees in each department

        Map<String, Long> departmentCounts = employees.stream()
                .collect(Collectors.groupingBy
                        (Employee::getDepartment, Collectors.counting()));
        //System.out.println(departmentCounts);
    }
}
