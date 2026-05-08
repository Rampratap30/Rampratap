package com.collection;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/*
Fail-fast iterators fail quickly by throwing a runtime exception as soon as they detect that the collection has been modified structurally during iteration.
Most general-purpose collection classes in Java (in java.util) use fail-fast iterators.
For example, the iterators of ArrayList, HashMap, HashSet, and Vector (when using Iterator) are all fail-fast. Under the hood,
these iterators leverage an internal modification counter (often called modCount) to track changes. This is as follows:

1) When a collection is created, modCount is initialised to zero.
2) Each structural modification (add, remove, set) increments this counter.
3) When an iterator is created, it captures the current modCount value as expectedModCount.
4) Before each iteration operation, the iterator compares modCount with expectedModCount.
5) If values differ, a ConcurrentModificationException is thrown immediately.

*/

public class FailFastExample {
    public static void main(String[] args) {
        //create a list
        List<String> list = new ArrayList<>();
        list.add("A");
        list.add("B");
        list.add("C");
        //Obtain Iterator (current modCount)
        Iterator<String> itr = list.iterator();

        while(itr.hasNext()){
            String element= itr.next();
            System.out.println("Processing ::"+element);
            if("B".equals(element)){
                // structural modification – triggers fail-fast behaviour.
                System.out.println("Adding element D::");
                list.add("D");
            }
        }
    }
    // When the loop reaches the modification,
    // the next call to iterator.next() fails with a ConcurrentModificationException,
    // because the iterator noticed that modCount changed.
}
