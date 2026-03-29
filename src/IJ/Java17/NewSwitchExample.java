package com.async.Java17;

public class NewSwitchExample {
    // Java 17 introduces Pattern Matching for switch, which:
    // ✔ Eliminates explicit type casting.
    // ✔ Allows switch to work with objects beyond primitives and enums.
    static void process(Object obj){
        switch (obj) {
            case Integer i -> System.out.println("Integer: " + i);
            case String s -> System.out.println("String: " + s);
            case Double d -> System.out.println("Double: " + d);
            default -> System.out.println("Unknown type");
        }
    }
    public static void main(String[] args) {
        process(42);          // Output: Integer: 42
        process("Hello");     // Output: String: Hello
        process(3.14);       // Output: Double: 3.14
        process(true);       // Output: Unknown type

        String json = """
        {
          "name": "Alice",
          "age": 25,
          "city": "New York"
        }
        """;
        System.out.println(json);
    }
}
