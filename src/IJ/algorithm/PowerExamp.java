package com.async.algorithm;

public class PowerExamp {
    public static void main(String[] args) {
        int base=2;
        int exp= 2;
        int result = power(base, exp);
        System.out.println(result);
    }

    private static int power(int base,int exp) {
        if(exp==0){
            return 1;
        }
        return base*power(base, exp-1);
    }

}
