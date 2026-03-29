package com.async.Java8;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class SortedOrder {
    public static void main(String[] args) {
        List<Integer> numbers= Arrays.asList(5,3,1,6,2,4);
        System.out.println("Original Number ::->"+numbers);
        List<Integer> sortedOrder= numbers.stream().sorted(Comparator.reverseOrder()).collect(Collectors.toList());
        System.out.println("Greater to Lowest Sorted Order ::->"+sortedOrder);

        List<Integer> lowToGreater = numbers.stream().sorted().collect(Collectors.toList());
        System.out.println(lowToGreater);

        //Is List as String type map(Integer::parseInt)
        //Max number map(Integer::Compare).orElseThrow()

        List<String> names = Arrays.asList("Alice", "Bob", "Annie", "Alex", "Charlie");

        long startCount = names.stream().filter(n->n.startsWith("A")).count();
        System.out.println("Start Count ::---"+startCount);
        long endCount = names.stream().filter(n->n.endsWith("x")).count();
        System.out.println("End Count ::---"+endCount);

        //Sum of Number in a List
        int sum= numbers.stream().mapToInt(Integer::intValue).sum();
        System.out.println("Sum::->"+sum);
    }
}
