package com.async.algorithm;

public class FindNumberIndex {
    public static void main(String[] args) {
        int [] array = {20,10,30,50,40,60};

        int target=40;

        int result = findNumberIndexs(array,target);
        System.out.println(result);
    }

    private static int findNumberIndexs(int[] array, int target){
        if(array.length==0){
            return 0;
        }
        int temp=0;
        for(int i=0;i< array.length;i++){
            if(array[i]==target){
                temp = i;
            }
        }
        return temp;
    }
}
