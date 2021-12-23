package com.sort;

public class UsingLoop {

    public static void main(String[] args) {
        int arr[] = {3,3,5,6,7,-1,2,1,0};
        for(int i = 0;i<arr.length;i++){
            for(int j =i+1;j<arr.length;j++){
                int temp = 0;
                if(arr[j]<arr[i]){
                    temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }
            }
            System.out.print(arr[i]+" ");
        }
    }
}
