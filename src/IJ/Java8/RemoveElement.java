package com.async.Java8;

import java.util.Arrays;

public class RemoveElement {
    public static void main(String[] args) {
        int[] arr= { 3, 9, 2, 3, 1, 7, 2, 3, 5 };
        int target= 3;

        int[] result  = removeElements(arr, target);
        System.out.println(Arrays.toString(result));

        String str ="Geeks";
        String original = str.toString();
        String  revers = new StringBuilder(original).reverse().toString();
        System.out.println(revers);


    }
    private static int[] removeElements(int[] arr, int target) {
        int aa =0;
        for (int i = 0; i < arr.length; i++) {
            if(arr[i] !=target){
             arr[aa++] = arr[i];
            }
        }
        return Arrays.copyOf(arr, aa);
    }
}
