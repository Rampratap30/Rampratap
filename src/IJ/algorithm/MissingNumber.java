package com.async.algorithm;

public class MissingNumber {
    public static void main(String[] args) {
        int[] array ={1,2,3,4,6};

        int result = missingNo(array);
        System.out.println(result);
    }

    private static int missingNo(int[] array) {

        int n = array.length+1;
        int expectedSum=(n*(n+1))/2;

        int actualSum = 0;
        for (int number:array){
            actualSum +=number;
        }
        return expectedSum-actualSum;
    }


}
