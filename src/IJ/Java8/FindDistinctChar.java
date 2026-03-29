package com.async.Java8;

import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

public class FindDistinctChar {
    public static void main(String[] args) {
        String str="abcdABCDabcd";
        System.out.println(reverse(str));

        char[] chars= str.toCharArray();
        Map<Character, Integer> charCount=new HashMap<>();

        for (char c: chars){
            if(charCount.containsKey(c)){
                charCount.put(c,charCount.get(c)+1);
            }else{
                charCount.put(c,1);
            }
        }
        //System.out.println(charCount);

        Map<Character,Long> mapCount = str.chars().mapToObj(c->(char)c).collect(Collectors.groupingBy(c->c,Collectors.counting()));
        //System.out.println(mapCount);

    }

    private static String reverse(String str){
        if(str.isEmpty()){
            return str;
        }else{
            return reverse(str.substring(1))+str.charAt(0);
        }

    }
}
