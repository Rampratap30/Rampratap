package com.leetcode.easy;


/*
Complexity Analysis
Time Complexity: O(n), where n is the length of the array. We perform a single pass through the array.
Space Complexity: O(1). No additional data structures (like a Set or another array) are used; the modification happens directly in the input array
 */
public class RemoveDuplicateArray {
    public static void main(String[] args) {

        int[] arr= {0,0,1,1,1,2,2,3,3,4};

        int result = removeDuplicate(arr);

        System.out.println(result);




    }

    private static int removeDuplicate(int[] arr) {

        if(arr.length==0) return 0;
        int j=1;
        for (int i = 1; i < arr.length; i++) {
            if(arr[i] !=arr[i-1]){
                arr[j] = arr[i];
                j++;
            }

        }
        return j;
    }
}
