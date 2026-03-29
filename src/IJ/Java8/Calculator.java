package com.async.Java8;

public class Calculator {
    public static void main(String[] args) {
        // Real-time use: Pass behavior (addition or multiplication) as a parameter
        ArithmeticOperation addition = (a, b) -> a + b;
        ArithmeticOperation multiplication = (a, b) -> a * b;

        System.out.println("Sum: " + addition.operate(5, 3)); // Output: Sum: 8
        System.out.println("Product: " + multiplication.operate(5, 3)); // Output: Product: 15
    }
}


