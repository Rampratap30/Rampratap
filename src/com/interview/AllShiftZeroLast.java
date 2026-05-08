package com.interview;

import java.util.Arrays;

public class AllShiftZeroLast {
    public static void main(String[] args) {
        int[] arr={1,0,2,3,0,4,0,5};
        int k = 0;
        for (int i = 0; i < arr.length; i++) {
            if(arr[i]!=0){
                arr[k++]= arr[i];
            }
        }
        while(k < arr.length){
            arr[k++]=0;
        }

        System.out.println(Arrays.toString(arr));
    }
}
