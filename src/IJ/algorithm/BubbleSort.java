package com.async.algorithm;

import java.util.Arrays;
import java.util.List;

public class BubbleSort {
    public static void main(String[] args) {
        int[] numbers = {5,2,8,12,3};
        bubbleSort(numbers);
        for (int num : numbers ) {
            System.out.print(num+" ");
        }

    }

    private static void bubbleSort(int[] numbers) {
        int n = numbers.length-1;
        for (int i = 0; i < n ; i++) {
            for (int j = 0; j <n-i-1 ; j++) {
                if (numbers[j]<numbers[j+1]){
                    //Swap
                    int temp = numbers[j];
                    numbers[j] =  numbers[j+1];
                    numbers[j+1]  = temp;
                }
            }

        }
    }
}
