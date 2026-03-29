package com.async.Java8;

import java.util.Arrays;

public class ReversArray {
    public static void main(String[] args) {
        int[] inputArray={10,20,30,40,50};

        revers(inputArray);
        System.out.println(Arrays.toString(inputArray));

    }

    private static void revers(int[] inputArray) {

        int left=0;
        int right= inputArray.length-1;

        while(left<right){
            //swap the value at the left and right indicate using a temporary variable.
            int temp= inputArray[left];
            inputArray[left]=inputArray[right];
            inputArray[right]= temp;

            // Move the pointer inward
            left++;
            right--;
        }
    }
}
