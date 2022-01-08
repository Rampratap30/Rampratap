package com.interview;

public class RemoveNumberSpecial {
    public static void main(String[] args)
    {
        String str = "3157g08#62%fA";
        String afterReplace  = str.replaceAll("[^A-Za-z0-9]", "");
        System.out.println(afterReplace.replaceAll("[(a-zA-Z13579)]",""));
    }
}
