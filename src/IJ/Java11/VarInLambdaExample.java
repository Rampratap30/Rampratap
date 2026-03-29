package com.async.Java11;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.util.List;

@Retention(RetentionPolicy.RUNTIME)
@interface NotNull {}
public class VarInLambdaExample {

    public static void main(String[] args) {
        List<String> names = List.of("Alice", "Bob", "Charlie");

        // Using 'var' to annotate parameters
        names.forEach((@NotNull var name) -> System.out.println(names));
    }
}
