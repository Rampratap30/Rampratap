package com.interview;

public class RemoveNumberSpecial {
    public static void main(String[] args)
    {
        String str = "3157g0862fA";
        String afterReplace  = str.replaceAll("([a-zA-Z13579])", "");
        System.out.println(afterReplace);
    }
}
