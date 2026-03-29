package com.async.algorithm;

public class FibonacciExamp {
    public static void main(String[] args) {
        int input = 3;

        int result = Fibonacci(input);
        System.out.println(result);
    }

    private static int Fibonacci(int input) {
        if(input<0){
            return -1;
        }
        if(input==0||input==1){
            return input;
        }
        return  Fibonacci(input-1)+Fibonacci(input-2);
    }


}
