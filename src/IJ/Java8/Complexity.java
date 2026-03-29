package com.async.Java8;

public class Complexity {
    public static void main(String[] args) {
        //System.out.println(sumNumbers(3));
        System.out.println(pairSumSequence(3));
    }

    //Space Complexity 0(n)
    private static int sumNumbers(int n) {
        if(n<=0){
            return 0;
        }
        return n+sumNumbers(n-1);
    }

    //Space Complexity 0(1)
    private static int pairSumSequence(int n){
        int total =0;
        for(int i=0;i<=n;i++){
            total = total+pairSum(i, i+1);
        }
        return total;
    }

    private static int pairSum(int a, int b) {
        return a+b;
    }


}
