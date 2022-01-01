package com;

import java.util.Arrays;

public class MoveAllZeroStart {
    public static void main(String[] args) {
        // TODO Auto-generated method stub

        Integer fullArray[] = { 1, 10, 20, 0, 59, 63, 0, 88, 0 };

        for (int i = 0; i <= fullArray.length - 1; i++)  {
            if (fullArray[i] == 0 && i > 0) {
                int temp = fullArray[i - 1];
                if (temp != 0) {
                    fullArray[i - 1] = 0;
                    fullArray[i] = temp;
                    i = -1;
                }
            }
        }
        System.out.print(Arrays.asList(fullArray).toString());
        System.out.println("");

        int[] num={1,2,5,0,0,0,4,3};
        for(int i=0;i<num.length;i++){
            if(num[i]==0){
                int k=num[i];
                for(int j=0; j<=i ; j++){
                    num[j]+=k;
                    k = num[j]-k;
                    num[j]-=k;
                }
            }
        }
       /* for(int i = 0;i<num.length;i++)
            System.out.print(num[i]+"\t");*/


        int[] nums={1,2,5,0,0,0,4,3};
        int temp = 0;
        for(int i=0;i<nums.length;i++){
            for(int j = 1 ;j<(nums.length-i);j++){
                if(nums[j-1] > nums[j]){
                    temp = nums[j-1];
                    nums[j-1] = nums[j];
                    nums[j] = temp;
                }
            }
        }
        for(int i = 0;i<nums.length;i++)
            System.out.print(nums[i]+"\t");


    }
}
