package com.collection;

import java.util.Collections;
import java.util.LinkedList;

public class ReversLinkList1 {
    public static void main(String[] args) {
        // Declaring linkedlist without any initial size
        LinkedList<Integer> linkedli = new LinkedList<Integer>();
        // Appending elements at the end of the list
        linkedli.add(new Integer(1));
        linkedli.add(new Integer(2));
        linkedli.add(new Integer(3));
        linkedli.add(new Integer(4));
        linkedli.add(new Integer(5));
        System.out.print("Elements before reversing: " + linkedli);
       // linkedli = reverseLinkedList(linkedli);
        Collections.reverse(linkedli);
        System.out.print("\nElements after reversing: " + linkedli);

    }

    private static LinkedList<Integer> reverseLinkedList(LinkedList<Integer> llist) {

        for (int i = 0; i < llist.size() / 2; i++) {
            Integer temp = llist.get(i);
            llist.set(i, llist.get(llist.size() - i - 1));
            llist.set(llist.size() - i - 1, temp);
        }
        return llist;
    }
}
