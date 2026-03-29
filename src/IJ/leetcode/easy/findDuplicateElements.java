package com.async.leetcode.easy;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class findDuplicateElements {
    public static void main(String[] args) {
        // Initial stream
        Stream<Integer> stream
                = Stream.of(2, 17, 5,
                20, 17, 30,
                4, 23, 59, 23);
        System.out.println(findDuplicateElement(stream));
    }

    private static<T> Set<T> findDuplicateElement(Stream<T> stream) {

        Set<T> items = new HashSet<>();
        return stream.filter(n->!items.add(n)).collect(Collectors.toSet());

    }
}
