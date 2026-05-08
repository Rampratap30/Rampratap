package com.dsa;

import java.util.Arrays;

public class TwoSumPairSum {
    public static void main(String[] args) {
        int[] arr = { 0, -1, 2, -3, 1 };
        int target = -2;

        if(twoSumBinarySearch(arr, target)){
            System.out.println("true");
        }else{
            System.out.println("false");
        }
    }
    //Generating all Possible Pairs - O(n2) time and O(1) space
    private static boolean twoSumPair(int[] arr, int target) {
        for (int i = 0; i < arr.length ; i++) {
            for (int j = i+1; j < arr.length; j++) {
                if(arr[i]+arr[j]==target){
                    return true;
                }
            }
        }
        return false;
    }

    //Sorting and Binary Search - O(n × log(n)) time and O(1) space

    private static boolean twoSumP(int[] arr,int target){
        Arrays.sort(arr);

        for (int i = 0; i < arr.length; i++) {
            int complement = target-arr[i];

            if(binarySearch(arr,i+1,arr.length-1,complement)){
                return false;
            }
        }
        return true;
    }

    private static boolean binarySearch(int[] arr, int left, int right, int target) {
        while(left < right){
            int mid = left+(right-left)/2;

            if(arr[mid]==target){
                return true;
            }else if(arr[mid]<target){
                left = mid+1;
            }else{
                right = mid-1;
            }
        }
        return false;
    }

    //Sorting and Two-Pointer Technique - O(n × log(n)) time and O(1) space

    private  static boolean twoSumBinarySearch(int[] arr, int target){
        Arrays.sort(arr);

        int left =0, right = arr.length-1;

        while(left < right){

            int sum = arr[left]+arr[right];

            if(sum==target){
                return true;
            }else if(sum <target){
                left++;
            }else{
                right--;
            }
        }
        return false;
    }

}
