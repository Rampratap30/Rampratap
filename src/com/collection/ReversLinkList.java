package com.collection;

import java.util.LinkedList;

public class ReversLinkList {
    public static void main(String[] args) {
        // Declaring linkedlist without any initial size
        LinkedList<String> linkedli = new LinkedList<String>();
        // Appending elements at the end of the list
        linkedli.add("Cherry");
        linkedli.add("Chennai");
        linkedli.add("Bullet");
        linkedli.add("Bullets");
        System.out.print("Elements before reversing: " + linkedli);
        linkedli = reverseLinkedList(linkedli);
        System.out.print("\nElements after reversing: " + linkedli);

    }

    private static LinkedList<String> reverseLinkedList(LinkedList<String> llist) {

        LinkedList<String> revLinkedList = new LinkedList<String>();
        for (int i = llist.size() - 1; i >= 0; i--) {
            revLinkedList.add(llist.get(i));
        }
        return revLinkedList;
    }
}
