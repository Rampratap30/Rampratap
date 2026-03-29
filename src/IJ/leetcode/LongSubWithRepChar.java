package com.async.leetcode;

import java.util.HashSet;

public class LongSubWithRepChar {
    public static void main(String[] args) {
        String str="abcabcbb";
        int legnOfCountResult = lengthOfLongestSubstring(str);
        System.out.println(legnOfCountResult);
    }

    private static int lengthOfLongestSubstring(String str) {
        int result = 0;
        for (int i = 0; i < str.length(); i++) {
            for (int j = i; j < str.length(); j++) {
                if(is_unique_within_range(str,i,j)){
                    result = Math.max(result, j-i+1);
                }
            }
        }
        return result;
    }

    private static boolean is_unique_within_range(String str, int start, int end) {
        HashSet<Character> hset = new HashSet<>();
        for (int i = start; i <= end; i++) {
            char ch = str.charAt(i);
            if(hset.contains(ch)){
                return false;
            }
            hset.add(ch);
        }
        return true;
    }
}
