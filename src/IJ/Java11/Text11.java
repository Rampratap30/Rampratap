package com.async.Java11;

import java.util.stream.Collectors;

public class Text11 {
    public static void main(String[] args) {
        String str="";
        System.out.println(str.isBlank());
        String str1="Text";
        System.out.println(str1.isBlank());

        //-----------------------------------------------

        // lines(): This method is to return a collection of strings that are divided by line terminators

        String str2 = "Geeks\nFor\nGeeks";
        System.out.println(str2.lines().collect(Collectors.toList()));

        //repeat(n): Result is the concatenated string of original string repeated the number of times in the argument.
        String str3 = "GeeksForGeeks";
        System.out.println(str3.repeat(4));

        //stripLeading(): It is used to remove the white space which is in front of the string

        String str4 = " GeeksForGeeks";
        System.out.println(str4.stripLeading());

        //stripTrailing(): It is used to remove the white space which is in the back of the string
        String str5 = " GeeksForGeeks";
        System.out.println(str5.stripLeading());

        //strip(): It is used to remove the white spaces which are in front and back of the string

        String str6 = " GeeksForGeeks ";
        System.out.println(str6.strip());


    }
}
