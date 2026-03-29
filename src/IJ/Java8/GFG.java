package com.async.Java8;

public class GFG {
    // Main driver method
    public static void main(String args[])
    {
        // Declaring and initializing rows and columns
        // For square row = columns

        // Custom input initialization values
        int rows = 8, columns = 22;

        // Calling the method1 to print hollow rectangle
        // pattern
        print_rectangle(rows, columns);

    }

    private static void print_rectangle(int rows, int columns) {

        int a,b;
        // Outer loop for rows
        for (a = 1; a <= rows; a++) {
            // Inner loop for columns
            for (b = 1; b <= columns; b++) {
                // Condition to check for boundary
                if (a == 1 || a == rows || b == 1 || b == columns) {
                    System.out.print("*");
                } else {
                    System.out.print(" ");
                }
            }
            // New line after each row
            System.out.println();
        }
    }
}
