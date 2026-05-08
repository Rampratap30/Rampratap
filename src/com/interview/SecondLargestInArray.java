package com.interview;

public class SecondLargestInArray {
    public static void main(String[] args) {
        int[] numbers = {4, 8, 1, 2, 9, 3};
        int firstLargest=Integer.MIN_VALUE;
        int secondLargest=Integer.MIN_VALUE;

        for(int num: numbers){
            if(num> firstLargest){
                secondLargest = firstLargest;
                firstLargest=num;
            }else if(num>secondLargest && num != firstLargest){
                    secondLargest = num;
            }
        }
        System.out.println("Second Largest element is "+secondLargest);
    }
}
