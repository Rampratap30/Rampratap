package com.async.algorithm;

public class PairMaxProduct {
    public static void main(String[] args) {
        int[] array ={10,20,30,40,50};

        String result = maxPair(array);
        System.out.println(result);
    }

    private static String maxPair(int[] array) {
        int maxProduct=0;
        String pair="";
        for(int i=0;i<array.length;i++){
            for(int j=i+1;j<array.length;j++){
                if(array[i]*array[j]>maxProduct){
                    maxProduct= array[i]*array[j];
                    pair = Integer.toString(array[i])+","+Integer.toString(array[j]);
                }
            }
        }
        return pair;
    }


}
