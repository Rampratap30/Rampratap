package com.async.algorithm;

public class IsUniques {
    public static void main(String[] args) {
        int[] arrInput = {1,2,3,4};

        boolean check = isUnique(arrInput);
        System.out.println(check);
    }

    private static boolean isUnique(int[] array){
        for (int i = 0; i < array.length ; i++) {
            for (int j = i+1; j < array.length ; j++) {
                if(array[i]==array[j]){
                    return false;
                }
            }
        }
        return true;
    }
}
