package com.async.Java8;

import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Predicate;
import java.util.stream.Collectors;

public class Functional_Predicate {
    public static void main(String arg[]) {
        List<Integer> number = Arrays.asList(1, 2, 3, 4, 5, 6);
        // * Predicate<T>: Represents a condition that takes an input and returns a boolean value.
        Predicate<Integer> isEven = num -> num % 2 == 0;

        // Using Predicate in a stream to filter even numbers
        List<Integer> evenNumbers = number.stream().filter(isEven).collect(Collectors.toList());

        System.out.println(evenNumbers); // Output: [2, 4, 6]



        //Consumer<T>: Represents an operation that accepts a single input and returns no result.
        //Real-time Example: Performing an action on each element of a collection, such as printing all elements to the console, saving data to a database, or updating a display.

        List<String> names = Arrays.asList("Tom", "Jerry", "Spike");
        Consumer<String> printName = name -> System.out.println("Hello, " + name);

        // Using Consumer with List.forEach()
        names.forEach(printName);
        // Output:
        // Hello, Tom
        // Hello, Jerry
    }
}
