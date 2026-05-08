package com;

import java.util.Scanner;

public class Problem {

    public static void main(String[] args) {

//        Scanner in = new Scanner(System.in);
//
//        // input for textInput
//        String textInput = in.nextLine();
//
//        int result = editorMiss(textInput);
//        System.out.print(result);
        String s = "abc";
        String s1 ="abcdef";

        System.out.println(s.equalsIgnoreCase(s1));
        System.out.println(s == s1);
    }

    private static int editorMiss(String textInput) {
        int  answer = 0;
        // Write your code here

        String[] counts = textInput.split(" ");
        for(int i = 0;i<3;i++) {
            answer++;
        }
        return answer;
    }
}
