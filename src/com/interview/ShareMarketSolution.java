package com.interview;

public class ShareMarketSolution {
    public static void main(String[] args) {
        int[] prices = {2,4,1};

        int sum = 0;   // Stores the maximum profit
        int buy = 0;   // Index to track the minimum buying price

        // Iterate through the stock prices starting from the second day
        for (int i = 1; i < prices.length; i++) {
            // If selling today gives a profit, update max profit
            if (prices[i] - prices[buy] > 0) {
                sum = Math.max(sum, prices[i] - prices[buy]);
            } else {
                // If a lower price is found, update the buying index
                buy = i;
            }
        }

        System.out.println(sum);
    }
}
