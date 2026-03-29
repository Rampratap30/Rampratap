package com.async.Java8;

import java.util.Map;
import java.util.stream.Collectors;

public class CountRepeatedCharsStreams {
    public static void main(String[] args) {
        String inputString = "programming is awesome";

        Map<Character, Long> charCounts = inputString.chars()
                .mapToObj(c->(char) c)
                .filter(c-> !Character.isWhitespace(c))//ignore Space
                .collect(Collectors.groupingBy(c->c, Collectors.counting()));

        System.out.println("Repeated characters and their counts using Java 8 Streams:");

        System.out.println("Repeated characters and their counts using Java 8 Streams:"+charCounts);


        charCounts.forEach((character, count)->{
            if(count>0){
                System.out.println("'" + character + "': " + count + " times");
            }
        });
    }
}
