package com.async.leetcode;

import java.util.regex.Pattern;

public class PatternExample {
    public static void main(String[] args) {
        System.out.println(Pattern.matches("a", "aa"));
        System.out.println(Pattern.matches("a*", "aa"));
        System.out.println(Pattern.matches(".*", "ab"));
    }
}
