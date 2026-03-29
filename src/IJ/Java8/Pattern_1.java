package com.async.Java8;

public class Pattern_1 {
    public static void main(String args[]) {
        int n = 6;
        //printPattern(n);
//        System.out.println();
//        printPatternReverse(n);
//
//        System.out.println();
//        printPatternReverse2(n);
//
//        System.out.println();
        printPatternReverse3(n);
    }

    /*

     *
     * *
     * * *
     * * * *
     * * * * *
     * * * * * *

    */
    private static void printPattern(int n) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    /*

     * * * * * *
     * * * * *
     * * * *
     * * *
     * *
     *

     */
    private static void printPatternReverse(int n) {
        for (int i = n; i >= 1; i--) {
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    private static void printPatternReverse2(int n) {
        for (int i = 1; i <= n; i++) {
            for (int j = n; j >= i; j--) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    private static void printPatternReverse3(int n) {
        int i, j;

        // outer loop to handle number of rows
        for (i = 1; i <= n; i++) {

            // inner loop to print the spaces
            for (j = 1; j <= 2 * (n - i); j++) {
                System.out.print(" ");
            }

            // inner loop to print the first part
            for (j = i; j >= 1; j--) {
                System.out.print(j + " ");
            }

            // inner loop to print the second part
            for (j = 2; j <= i; j++) {
                System.out.print(j + " ");
            }

            // printing new line for each row
            System.out.println();
        }
    }
}
