package com.collection;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class PerformanceComparisonFFFS {

    private static final int ITERATIONS = 1_000_000;
    public static void benchmarkFailFast() {
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < ITERATIONS; i++) {
            list.add(i);
        }

        long startTime = System.nanoTime();
        for (Integer value: list) {
            // Simulate processing
            Math.sqrt(value);
        }
        long endTime = System.nanoTime();

        System.out.println("Fail-fast iteration time: " +
                (endTime - startTime) / 1_000_000 + " ms");
    }

    public static void benchmarkFailSafe() {
        CopyOnWriteArrayList<Integer> list = new CopyOnWriteArrayList<>();
        for (int i = 0; i < ITERATIONS; i++) {
            list.add(i);
        }

        long startTime = System.nanoTime();
        for (Integer value: list) {
            // Simulate processing
            Math.sqrt(value);
        }
        long endTime = System.nanoTime();

        System.out.println("Fail-safe iteration time: " +
                (endTime - startTime) / 1_000_000 + " ms");
    }


    public static void main(String[] args) {
        benchmarkFailFast();
        benchmarkFailSafe();
    }
}
