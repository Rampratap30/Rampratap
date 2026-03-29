package com.async.Java8;

public class SecondHighest {
    public static void main(String[] args) {
        int[] array ={100,750,800,250,500};

        int highest= Integer.MIN_VALUE;
        int secondHighest = Integer.MAX_VALUE;

        for (int i = 0; i < array.length; i++) {
            if(array[i]>highest){
                secondHighest = highest;
                highest = array[i];
            }else if(array[i]>secondHighest){
                secondHighest = array[i];
            }
        }
        System.out.println("Highest Salary::->"+highest);
        System.out.println("Second Highest Salary::->"+secondHighest);

    }
}
