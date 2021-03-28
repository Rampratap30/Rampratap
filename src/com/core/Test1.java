package com.core;

import java.util.PriorityQueue;

public class Test1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		PriorityQueue toDo = new PriorityQueue();
		toDo.add("1");
		toDo.offer("2");
		System.out.println(toDo.size() +" "+ toDo.poll());
		System.out.println(" "+ toDo.peek());
		//System.out.println(toDo.size() +" "+ toDo.poll());
	}

}
