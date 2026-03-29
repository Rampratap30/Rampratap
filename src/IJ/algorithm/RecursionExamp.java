package com.async.algorithm;

public class RecursionExamp {
    public static void main(String[] args) {
        int input = 3;

        int result = recursion(input);
        System.out.println(result);
    }

    private static int recursion(int input) {
        if(input<0){
            return 0;
        }
        if(input==0||input==1){
            return 1;
        }
        return input* recursion(input-1);
    }


}
