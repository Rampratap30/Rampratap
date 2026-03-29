package com.async.algorithm;

public class DecimalToBinaryExamp {
    public static void main(String[] args) {
        int input=30;
        int result = dicimalToBinary(input);
        System.out.println(result);
    }

    private static int dicimalToBinary(int input) {
        if(input==0){
            return 0;
        }
        return input%2+10*dicimalToBinary(input/2);
    }

}
