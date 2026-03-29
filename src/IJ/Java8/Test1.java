package com.async.Java8;

import java.util.*;
import java.util.stream.Collectors;

import static java.util.stream.Collectors.collectingAndThen;
import static java.util.stream.Collectors.partitioningBy;

public class Test1 {
    public static void main(String[] args) {
        List<Integer> list= Arrays.asList(1, -3, 5, -2, 8, -4, 0, 0, 0, 0);
        //list.stream().sorted().forEach(System.out::print);
        Collections.sort(list);
        System.out.println("Sorted Order Without Stream::"+list);

        List<Integer> sortedNumberDescending = list.stream().sorted(Comparator.reverseOrder()).collect(Collectors.toList());

        System.out.println("Sorted Descending Order :: "+sortedNumberDescending);

        // Original list with the numbers including string representations
        List<String> originalStringList = Arrays.asList("1", "-3", "5", "-2", "8", "-4", "0", "0", "0", "0");

        // Convert the list of Strings to a List of Integers and sort using streams
        List<Integer> sortedNumber = originalStringList.stream().map(Integer::parseInt).sorted().collect(Collectors.toList());

        System.out.println("OriginalStringList ::"+originalStringList);
        System.out.println("SortedNumber Stream::"+sortedNumber);

        System.out.println("---------------------------------------");
        //Reverse Order
        String str="Hello";
        char[] chars= str.toCharArray();
        String reversed ="";
        for(int i = str.length()-1;i>=0;i--){
            reversed+= str.charAt(i);
        }
        System.out.println("Reverse order::---->"+ reversed);
        System.out.println("---------------------------------------");

        //Remove Duplicate
        List<Integer> removeDuplicate = Arrays.asList(1,2,4,5,6,2,4,3);
        removeDuplicate.stream().distinct().sorted().forEach(System.out::print);

        System.out.println();
        List<String> removeStringDuplicate = Arrays.asList("1","2","4","5","6","2","4","3");

        List<Integer> finalDuplicateList= removeStringDuplicate.stream().distinct().map(Integer::parseInt).sorted().collect(Collectors.toList());

        System.out.println("Remove Duplicate::"+finalDuplicateList);
        System.out.println("---------------------------------------");

        //separationOfEvenOddNumberInList

        List<Integer> oneToTen = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        Collection<List<Integer>> evenOddList = oneToTen.stream()
                .collect(collectingAndThen(partitioningBy(i -> i % 2 == 0),
                        Map::values));

        System.out.println(evenOddList);

        Map<Boolean, List<Integer>> evenAddOddSeparation = oneToTen.stream()
                .collect(partitioningBy(i -> i % 2 == 0));

        System.out.println(evenAddOddSeparation);

        System.out.println("---------------------");
        //

        List<Integer> lists = Arrays.asList(10,15,8,49,25,98,98,32,15);

        Collections.sort(lists);
        System.out.println("List::::->"+lists);

        List<Integer> result= lists.stream().sorted(Comparator.reverseOrder()).collect(Collectors.toList());
        System.out.println("Result::::->"+result);


        // Stream will convert in to stream
//        lists.stream()
//                .sorted(Comparator.reverseOrder())
//                .forEach(System.out::print);


        List<String> listss = Arrays.asList("java scala ruby", "java react spring java");
        List<String> resultList = listss.stream().map(String::toUpperCase).collect(Collectors.toList());
        System.out.println("resultList::::->"+resultList);

        //Check 
        boolean check = listss.stream().anyMatch(s->s.contains("javaa"));
        System.out.println("Check Boolean::->"+check);

        //Find the Longest String
        String longest = listss.stream()
                .reduce((word1, word2) -> word1.length() > word2.length() ? word1 : word2)
                .orElse(null);
        System.out.println(longest);


        System.out.println("-------------------------------------------------------------------");
        //Filter Odd Number from List
        List<Integer> numbers = Arrays.asList(1,2,3,4,5,6);
        List<Integer> oddNumber = numbers.stream().filter(n->n%2!=0).collect(Collectors.toList());
        System.out.println("Odd Number::->"+oddNumber);


        // Find MaxNumber from List

        int maxNumber = numbers.stream().max(Integer::compare).orElseThrow();
        System.out.println("MaxNumberfrom List::->"+maxNumber);

        //

    }



}
