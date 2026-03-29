package com.async.hacker;

import java.util.Arrays;
import java.util.List;

//Count Elements Greater Than Previous Average

public class CountGreaterElementsPre {
    public static void main(String[] args) {
        List<Integer> inputArr = Arrays.asList(100, 200, 150,300);
        int countResult = countGreaterElementPre(inputArr);
        System.out.println(countResult);
    }

    private static int countGreaterElementPre(List<Integer> inputArr) {
        if(inputArr == null || inputArr.size()==0){
            return 0;
        }
        int count = 0;
        long sum = inputArr.get(0);

        for (int i = 1; i < inputArr.size(); i++) {
            double previousAverage = (double) sum/i;
            if(inputArr.get(i) > previousAverage){
                count++;
            }
            sum+= inputArr.get(i);
        }
        return count;
    }
}
