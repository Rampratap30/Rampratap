package com.async.leetcode;

import java.util.ArrayList;
import java.util.List;

public class LetterCombinationPhone {
    public static void main(String[] args) {
        String digit ="2";
        List<String> result = letterCombinations(digit);
        System.out.println(result);

    }

    private static List<String> letterCombinations(String digits) {
        List<String> list = new ArrayList<>();
        if (digits.length() == 0) {
            return list;
        }
        list.add("");
        String[] d= new String[] {"abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
        for (char i: digits.toCharArray()) {
            String s = d[i - '2'];
            List<String> t = new ArrayList<>();
            for (String a : list) {
                for (String b : s.split("")) {
                    t.add(a + b);
                }
            }
            list = t;

        }
        return list;
    }
}
