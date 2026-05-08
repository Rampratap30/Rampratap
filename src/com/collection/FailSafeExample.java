package com.collection;

import java.util.Iterator;
import java.util.concurrent.CopyOnWriteArrayList;

/*
Fail-safe iterators take a different approach: they do not throw exceptions if the collection is modified during iteration
Because they avoid raising errors on modification
*/
public class FailSafeExample {
    public static void main(String[] args) {
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        list.add("Item1");
        list.add("Item2");
        list.add("Item3");

        // Iterator works on a snapshot of the current array
        Iterator<String> iterator = list.iterator();

        while (iterator.hasNext()) {
            String item = iterator.next();
            System.out.println("Processing: " + item);

            // This modification creates a new internal array
            // but doesn't affect the current iteration
            if ("Item2".equals(item)) {
                list.add("NewItem"); // Safe modification
            }
        }

        System.out.println("Final list: " + list);
        // Output: [Item1, Item2, Item3, NewItem]
    }
}
