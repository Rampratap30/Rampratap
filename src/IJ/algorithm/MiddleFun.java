package com.async.algorithm;

public class MiddleFun {
    public static void main(String[] args) {
        int[] arr={1, 2, 3, 4};

        int[] result = middle(arr);

        for (int i=1;i<result.length;i++){
            System.out.println(i);
        }


    }

    private static int[] middle(int[] array) {
        if (array.length <= 2) {
            return new int[0]; // Return an empty array if the input array has 2 or fewer elements
        }
        // Create a new array with a size of the input array length minus 2
        int[] middleArray = new int[array.length - 2];

        // Copy the elements from the input array, excluding the first and last elements
        int index = 1;
        while (index < array.length - 1) {
            middleArray[index - 1] = array[index];
            index++;
        }
        return middleArray;
    }
}
