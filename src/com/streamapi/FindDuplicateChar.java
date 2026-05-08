package com.streamapi;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class FindDuplicateChar {
    public static void main(String[] args) {
        String input = "vivek kadiyan";
        List<String> duplicateChars = findDuplicateChars(input);
        System.out.println("Duplicate character:::: "+duplicateChars);

        Map<Character,  Long> duplicates = input.chars().mapToObj(c->(char) c)
                .collect(Collectors.groupingBy(c->c,Collectors.counting()))
                .entrySet().stream().filter(entry->entry.getValue()>1)
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

        System.out.println(duplicates);
        /*
        Time Complexity: O(n).
        Benefit: Uses built-in groupingBy and counting collectors
        */

    }

    private static List<String> findDuplicateChars(String input) {
        return Arrays.stream(input.split("")).collect(Collectors.groupingBy(ch->ch,Collectors.counting()))
                .entrySet().stream().filter(ch->ch.getValue()>1)
                .map(in->in.getKey()).collect(Collectors.toList());
    }


}
