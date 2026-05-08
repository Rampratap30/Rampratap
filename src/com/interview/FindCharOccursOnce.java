package com.interview;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public class FindCharOccursOnce {
    public static void main(String[] args) {
        String str ="programming";

        Map<Character,Long> maps = str.chars().mapToObj(c->(char) c).
                collect(Collectors.groupingBy(
                        Function.identity(),
                        Collectors.counting()
                ));
        System.out.println(maps);

        List<Character> finalResult =maps.entrySet().stream().filter(
                c->c.getValue()==1).
                map(Map.Entry::getKey).toList();

        System.out.println(finalResult);

    }
}
