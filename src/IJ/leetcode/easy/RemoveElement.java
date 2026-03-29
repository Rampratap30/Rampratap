package com.async.leetcode.easy;

public class RemoveElement {
    public static void main(String[] args) {
        int [] arr= {3,2,2,3};
        int target = 3;

        int results = removeElements(arr,target);
        System.out.println(results);
    }

    private static int removeElements(int[] arr, int target) {
        if(arr.length==0) return 0;
        int validateElement=0;
        for(int currentElement:arr){
            if(currentElement !=target){
                arr[currentElement]= validateElement;
                validateElement++;
            }
        }
        return validateElement;
    }
}
