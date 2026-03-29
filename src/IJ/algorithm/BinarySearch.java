package com.async.algorithm;

public class BinarySearch {
    public static void main(String[] args) {
        int[] data ={10,20,30,40,50,60,80,90,};
        int target=60;

        int result = binarySearch(data,target);
        if(result==-1){
            System.out.println("Element not found in the array");
        }else{
            System.out.println("Element found in array ::->"+target+" at index position ::->"+result);
        }
    }

    private static int binarySearch(int[] data, int target){
        int left = 0;
        int right = data.length-1;

        while(left<=right){
            int mid = left+(right-left)/2;

            if(data[mid]==target){
                return mid;
            }else if(data[mid]< target){
                left=mid+1;
            }else{
                right= mid-1;
            }
        }
        return 0;
    }
}
