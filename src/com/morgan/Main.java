package com.morgan;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        List<User> list = Arrays.asList(new User("X", true), new User("Y", false),
                new User("Z", true), new User("A", true),
                new User("X", true) // Duplicate active user
        );

        // 1. Find all distinct active users and sort them alphabetically
        List<String> distinctActiveUsers = list.stream().filter(User::isActive)
                .map(User::getName)
                .distinct()
                .sorted()
                .collect(Collectors.toList());

        System.out.println("Distinct Active Users: " + distinctActiveUsers);

        // 2. Count active vs inactive users
        Map<Boolean,Long> counts= list.stream()
                .collect(Collectors.groupingBy(
                        User::isActive,
                        Collectors.counting()
                ));

        System.out.println("Active Count: " + counts.getOrDefault(true, 0L));
        System.out.println("Inactive Count: " + counts.getOrDefault(false, 0L));
    }
}
