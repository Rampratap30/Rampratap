package com.streamapi;

import java.util.Arrays;
import java.util.stream.Collectors;

public class CodingProblem {
    public static void main(String[] args) {
        Integer array[] = {1,1,0,1,0 };
        System.out.println(Arrays.stream(array).sorted().collect(Collectors.toList()));
        swapArrayElement(array);


        //All zero are shifted end

        moveZerosToEnd(array);


    }

    private static void moveZerosToEnd(Integer[] array) {
        int count =0;
        for (int i = 0; i < array.length; i++) {
            if(array[i]!=0){
                array[count++]=array[i];
            }
        }
        while(count<array.length){
            array[count++] = 0;
        }
        System.out.println(Arrays.toString(array));
    }

    private static void swapArrayElement(Integer[] array) {
        int left =0;
        for (int i = 0; i < array.length; i++) {
            if(array[i]==0){
                int temp = array[i];
                array[i] = array[left];
                array[left]= temp;
                left++;
            }
        }
        System.out.println(Arrays.toString(array));
    }


}
