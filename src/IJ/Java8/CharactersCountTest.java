package com.async.Java8;

import java.util.*;
import java.util.stream.Collectors;

public class CharactersCountTest {
    public static void main(String[] args) {
        String program = "JAVA PROGRAMMER";
        char[] strArray=  program.toCharArray();
        //Getting Distinct characters in strArray

        Set<Character> set = new TreeSet<>();
        for (char c :strArray){
            set.add(c);
        }
        //set.forEach(System.out::println);

        for (char c : set) {
            // Using Streams & Lambda Expressions in Java 8
            long count = program.chars().filter(ch->ch ==c).count();
            //System.out.println("Occurances of Character '" +c+ "' : " +count);
        }
//---------------------------------------------------------------------------------
        //Remove duplicate
        Integer[] array = {5, 10, 3, 7, 2, 10, 5};
        Integer[] distinct = Arrays.stream(array)
                .distinct()
                .toArray(Integer[]::new);
        //System.out.println("Distinct elements: " + Arrays.toString(distinct));

        List<Integer> lists = Arrays.asList(array);

        List<Integer> results = lists.stream().distinct().collect(Collectors.toList());
        System.out.println("Distinct Elements::---->"+results);

//----------------------------------------------------------------------------------
        //WordCount
        List<String> list = Arrays.asList("java scala ruby", "java react spring java");

        String find="java";
        long findCount= list.stream()
                        .flatMap(s -> Arrays.stream(s.split(" ")))
                .filter(w-> w.equals(find)).count();
        System.out.println("Occurrences of \"" + find + "\": " + findCount);
        System.out.println("----------------------------------------");
        // Starting with prefix
        String[] strings = {"java", "scala", "javascript", "ruby","spring","angular"};
        String prefix = "j";
        String[] filtered = Arrays.stream(strings)
                .filter(s -> s.startsWith(prefix))
                .toArray(String[]::new);
        System.out.println("Filtered strings: " + Arrays.toString(filtered));

        List<String> inputStr = Arrays.asList(strings);
        List<String> startPrefix= inputStr.stream().filter(s->s.startsWith(prefix)).collect(Collectors.toList());
        System.out.println("Start Prefix::"+startPrefix);

        List<String> endPrefix= inputStr.stream().filter(s->s.endsWith("x")).collect(Collectors.toList());
        System.out.println("End Prefix::"+startPrefix);

//---------------------------------------------------------------------------------------------------------------------


        // Stream To Map
        List<String> listNames = Arrays.asList("java", "scala", "javascript", "ruby");

        Map<String,Integer> mapToInt =  listNames.stream()
                .collect(Collectors.toMap(s->s,String::length));
        System.out.println("----->"+mapToInt);

        String intPutStr = "To dynamically manage and differentiate application properties across microservices";

        Map<Character, Long> result = intPutStr.chars()
                .mapToObj(c->(char) c)
                .filter(c-> !Character.isWhitespace(c))//ignore Space
                .collect(Collectors.groupingBy(c->c, Collectors.counting()));

        System.out.println(result);


    }
}
