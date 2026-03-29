package com.async.algorithm;

import java.util.Arrays;

public class ReverseArray {
    public static void main(String[] args) {
        int[] arrayInput={1,3,4,5};
        reversResult(arrayInput);
    }

    private static void reversResult(int[] arrayInput) {
        for (int i = 0; i < arrayInput.length/2 ; i++) {
            int other = arrayInput.length-i-1;
            int temp = arrayInput[i];
            arrayInput[i]= arrayInput[other];
            arrayInput[other]= temp;
        }
        System.out.println(Arrays.toString(arrayInput));
    }


}
