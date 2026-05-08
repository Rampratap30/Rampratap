package com.employee;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public class ConvertListToMap {
    public static void main(String[] args) {
        List<Employee> employees = Arrays.asList(
                new Employee(1, "John", "Doe", 30, "IT", 60000, 2015, "New York", "Male"),
                new Employee(2, "Alice", "Smith", 28, "HR", 55000, 2017, "Los Angeles", "Female"),
                new Employee(3, "Mike", "Johnson", 35, "Finance", 70000, 2010, "Chicago", "Male"),
                new Employee(4, "Ishan", "Kishan", 26, "IT", 80000, 2022, "Bihar India", "Male"),
                new Employee(4, "prithvi", "Shaw", 28, "Product Development", 90000, 2022, "Bihar India", "Male"),
                new Employee(4, "Aaksh", "Deep", 25, "Product Development", 70000, 2021, "Delhi India", "Male"),
                new Employee(1, "sehwag", "Doe", 38, "IT", 90000, 2012, "Noida India", "Male"),
                new Employee(1, "Ankita", "kohali", 38, "IT", 92000, 2011, "Gurugram India", "Female"),
                new Employee(1, "Ankita", "kohali", 38, "IT", 92000, 2011, "Gurugram India", "Female")
        );

        Map<Integer, Employee> convertResult = employees.stream()
                .collect(Collectors.toMap(
                        Employee:: getId,
                        Function.identity(),
                        (existing,replacement)-> replacement
                ));

        System.out.println(convertResult);
    }
}
