package com.async.leetcode.easy;

import java.lang.reflect.Array;
import java.util.Arrays;

public class RemoveDuplicateFromSortArray {

    public static void main(String[] args) {

        int [] num =  {2,1,1};
        int result = removeDuplicates(num);
        System.out.println(result);
    }

    private static int removeDuplicates(int[] num) {
        if(num.length==0) return 0;
        Arrays.sort(num);
        int count = 1;
        for(int i=1;i<num.length;i++){
            if(num[i] != num[i-1]){
                num[count++]= num[i];
            }
        }
        return count;
    }


}
