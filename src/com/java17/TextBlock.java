package com.java17;

/*
Problems in the Old Approach

-Manual concatenation (+) makes the code hard to read.
-Escape characters (\n) clutter the string.
-Indentation is inconsistent, affecting readability.

Text Blocks – Multi-line string literals (""")

By default, Text Blocks preserve indentation.
We can remove extra spaces using .stripIndent()normalizes indentation


 */
public class TextBlock {
    public static void main(String[] args) {
        String json = """
        {
            "name": "Jane Doe",
            "role": "Software Engineer"
        }
        """;
        System.out.println("Text Block ::"+json);
        System.out.println("---------------------------------------------");
        String sql = """
            SELECT *
            FROM employees
            WHERE department = 'HR';
            """;
        System.out.println(sql);
    }
}
