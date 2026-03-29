package com.async.Java8;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class IntervalMerging {
    public static void main(String[] args) {
        int[][] intervals = {{1,3}, {2,6}, {10,12}, {13,15}};

        int[][] results = mergeResult(intervals);
        System.out.println("Output::");
        for (int[] interval: results){
            System.out.println(" "+interval[0]+" "+interval[1]);
        }
    }

    private static int[][] mergeResult(int[][] intervals) {
        if(intervals.length==0){
            return new int[0][0];
        }
        //Sort by start time
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        List<int[]> merge = new ArrayList<>();
        merge.add(intervals[0]);

        for (int i = 0; i < intervals.length ; i++) {

            int[] currentInterval = intervals[i];
            int[] lastInterval = merge.get(merge.size()-1);

            if(currentInterval[0]<= lastInterval[1]){
                lastInterval[1] = Math.max(lastInterval[1], currentInterval[1]);
            }else{
                merge.add(currentInterval);
            }
        }
        return merge.toArray(new int[merge.size()][]);
    }
}
