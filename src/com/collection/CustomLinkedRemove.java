package com.collection;

import java.util.LinkedList;

public class CustomLinkedRemove {

	/*
	 * Node head; // head of list
	 * 
	 * public void printList() { Node tnode = head; while (tnode != null) {
	 * System.out.print(tnode.data+" "); tnode = tnode.next; } }
	 */
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		/* Start with the empty list */
        LinkedList llist = new LinkedList(); 
  
        llist.push(7); 
        llist.push(1); 
        llist.push(3); 
        llist.push(2); 
        llist.push(8); 
        
        System.out.println("\nCreated Linked list is: "); 
       // llist.printList();

	}

}
