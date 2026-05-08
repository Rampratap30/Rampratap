package com.interview;

import java.util.Arrays;
import java.util.List;

public class ReverseString {
    public static void main(String[] args) {
        String input = "Hello";
        String reverse="";
        for(int i=input.length()-1;i>=0;i--){
            reverse+= input.charAt(i);
        }
        System.out.println(reverse);

        int [] arr = {1,2,3,4,5};
        List<Integer> listBoxed = Arrays.stream(arr).boxed().toList();
        System.out.println(listBoxed);
        //List<Integer> result = listBoxed.stream().sorted().toList();

        List<Integer> listResult = listBoxed.stream().sorted((a,b)->b.compareTo(a)).toList();

        System.out.println(listResult);



    }
}
