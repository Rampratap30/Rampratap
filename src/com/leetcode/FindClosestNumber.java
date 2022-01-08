package com.leetcode;

public class FindClosestNumber {
    public static void main(String[] args)
    {
        int[] numbers = {6,5,10,1,3,4,2,14,11,12};
        int target = 12;
        for(int i =0; i<numbers.length; i++)
        {
            sum(numbers, i, numbers[i], target, String.valueOf(numbers[i]));
        }
    }

    private static void sum(int[] arr, int i, int sum, int target, String valueOf) {


        for(int j = i+1; j<arr.length; j++)
        {
            if(sum+arr[j] == target){
                    System.out.println(valueOf+" "+String.valueOf(arr[j]));
            }else{
                sum(arr, j, sum+arr[j],target,valueOf+" "+String.valueOf(arr[j]));
            }
        }
        }
    }
