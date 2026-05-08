package com.employee;

import java.util.*;
import java.util.stream.Collectors;

public class EmployeeScenario {
    public static void main(String[] args) {
        List<Employees> empList = new ArrayList<>();
        empList.add(new Employees(1, "Yanksha", 28, 123, "F", "HR", "Blore", 2020));
        empList.add(new Employees(2, "Francesca", 29, 120, "F", "HR", "Hyderabad", 2015));
        empList.add(new Employees(3, "Ramesh", 30, 115, "M", "HR", "Chennai", 2014));
        empList.add(new Employees(4, "Melanie", 32, 125, "F", "HR", "Chennai", 2013));

        empList.add(new Employees(5, "Padma", 22, 150, "F", "IT", "Noida", 2013));
        empList.add(new Employees(6, "Milad", 27, 140, "M", "IT", "Gurugram", 2017));
        empList.add(new Employees(7, "Uzma", 26, 130, "F", "IT", "Pune", 2016));
        empList.add(new Employees(8, "Ali", 23, 145, "M", "IT", "Trivandam", 2015));
        empList.add(new Employees(9, "Ram", 25, 160, "M", "IT", "Blore", 2010));


        // Group the Employees by city.

        Map<String, List<Employees>> listEmpCity = empList.stream().collect(Collectors.groupingBy(Employees::getCity));
        //System.out.println(listEmpCity);

        //Group the Employees by Age
        
        Map<Integer,List<Employees>> listEmpAge= empList.stream().collect(Collectors.groupingBy(Employees::getAge));
        //System.out.println(listEmpAge);

        //Find the count of male and female employees present in the organization

        Map<String, Long> noOfMaleAndFemaleEmployees = empList.stream().collect(Collectors.groupingBy(Employees::getGender,Collectors.counting()));
        System.out.println(noOfMaleAndFemaleEmployees);

        //Find the count of male and female present in each department

        Map<String,Map<String,Long>> genderMapInDept = empList.stream().
                collect(Collectors.groupingBy(Employees::getDeptName, Collectors.groupingBy(Employees::getGender,Collectors.counting())));

        System.out.println(genderMapInDept);

        System.out.println("--------------------------------------");

        //Print the names of all distinct departments in the organization.

        empList.stream().map(Employees::getDeptName).distinct().forEach(System.out::println);

        System.out.println("--------------------------------------");

        //Print employee details whose age is greater than 28 in the orzanisation.

        empList.stream().filter(e->e.getAge()> 28).collect(Collectors.toList()).forEach(System.out::println);

        System.out.println("--------------------------------------");

        // Find maximum age/oldest of employee in the organisation.

        OptionalInt maxs = empList.stream().mapToInt(Employees:: getAge).max();
        if(maxs.isPresent()){
            System.out.println("Maximum Age ::"+maxs.getAsInt());
        }

        Optional<Employees> oldestEmp = empList.stream().max(Comparator.comparingInt(Employees::getAge));
        Employees oldAge = oldestEmp.get();

        System.out.println("Oldest employee details:: \n" + oldestEmp);

        System.out.println("--------------------------------------");







    }

}
