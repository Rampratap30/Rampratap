package com.async.hacker;

import java.util.HashMap;
import java.util.Map;

public class LongestCharNotDuplicate {
    public static void main(String[] args) {
        String str="codingisawesome";

        int count = lengthOfLongestSubstring(str);
        System.out.println("Input: \"" + str + "\", Output: " + count);
    }

    private static int lengthOfLongestSubstring(String str) {
        if (str == null || str.length() == 0) {
            return 0;
        }

        Map<Character, Integer> lastSeen = new HashMap<>();
        int maxLength = 0;
        int left = 0;

        for(int right =0;right<str.length();right++){
            char currentChar = str.charAt(right);

            if(lastSeen.containsKey(currentChar) && lastSeen.get(currentChar) >=left){
                // Move the left pointer past the last occurrence
                left= lastSeen.get(currentChar)+1;
            }
            lastSeen.put(currentChar,right);

            maxLength = Math.max(maxLength,right-left+1);
        }
        return maxLength;
    }

}
