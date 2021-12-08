package com.comman;

interface Supplier<T>{
    T get();
    default String greet() {
        return "Hello, World ";
    }
    default String greet2() {
        return "Hello, World 2";
    }
}

public class FunctionalInterface  {

    public static void main(String[] args) {

    }


}
