package com.async.Java17;

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
