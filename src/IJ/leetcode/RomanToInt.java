package com.async.leetcode;

import java.util.HashMap;
import java.util.Map;

public class RomanToInt {
    public static void main(String[] args) {
        String str = "LVIII";
        int result = romanToIn(str);
        System.out.println(result);

    }

    private static int romanToIn(String intPut){
        Map<Character, Integer> romanMap =  new HashMap<>();
        romanMap.put('I',1);
        romanMap.put('V', 5);
        romanMap.put('X', 10);
        romanMap.put('L', 50);
        romanMap.put('C', 100);
        romanMap.put('D', 500);
        romanMap.put('M', 1000);

        int total =0;
        int n = intPut.length();
        // Iterate through the string, stopping before the last character
        for(int i=0;i<n-1;i++){
            //Get the value of the current and next character

            int currentVal = romanMap.get(intPut.charAt(i));
            int nextVal = romanMap.get(intPut.charAt(i+1));

            //if the current value is less than next
            if(currentVal<nextVal){
                total -=currentVal;
            }else {
                total+=currentVal;
            }
        }
        total+=romanMap.get(intPut.charAt((n-1)));
        return total;
    }
}

    
