package com.interview;

public class CountPairsWithDiff {

    public static void main(String[] args) {
        // TODO Auto-generated method stub
        int arr[] = {1, 5, 3, 4, 2};
        int n = arr.length;
        int k = 2;
        System.out.println("Count of pairs with given diff is "
                + countPairsWithDiffK(arr, n, k));
    }

    private static int countPairsWithDiffK(int[] arr, int n, int k) {

        int count = 0;
        for(int i= 0;i<arr.length;i++){
            for(int j = i+1;j<n;j++) {
                if (arr[i] - arr[j] == k || arr[j]-arr[i] == k){
                    count++;
                }
            }
        }
        return count;
    }
}
