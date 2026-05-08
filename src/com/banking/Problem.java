package com.banking;

public class Problem {
    public static void main(String[] args) {

        int[] arr={1,2,3,4,5,6};
        int target = 10;
        for(int i=0;i< arr.length;i++){
            sum(arr, i, arr[i], target, String.valueOf(arr[i]));
        }
    }

    private static void sum(int[] nums, int i, int sum, int target, String s) {

        for(int j= i+1;j<nums.length;j++){
            if(sum+nums[j] == target){
                System.out.println(s+" "+String.valueOf(nums[j]));
            }else{
                sum(nums, j, sum+nums[j],target, s+" "+String.valueOf(nums[j]));
            }
        }
    }







}
