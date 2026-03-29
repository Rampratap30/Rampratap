package com.async.Java8;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;

public class FirstNonRepeatedChar
{
    public static void main(String[] args) {
        String str="Rampratap";

        Character result1 = findFirstNonRepeatedCharacter(str.toLowerCase());
        System.out.println("First non-repeated character in \"" + str + "\": " + result1);
    }

    private static Character findFirstNonRepeatedCharacter(String str) {
        // 1. Count character frequencies and store them in a LinkedHashMap to preserve order.
        Map<Character, Long> charCounts = str.chars().mapToObj(c->(char)c).collect(Collectors.groupingBy(
            Function.identity(),
                LinkedHashMap::new,// Ensures insertion order is maintained
                Collectors.counting()

        ));
        System.out.println(charCounts);        // 2. Stream the map entries, filter for count == 1, and find the first one.

        Optional<Character> firstNonRepeat = charCounts.entrySet().stream()
                .filter(entry -> entry.getValue() == 1L)
                .map(Map.Entry::getKey)
                .findFirst(); // Retrieves the first matching character in order

        // 3. Return the character or null if none found
        return firstNonRepeat.orElse(null);

    }
}
