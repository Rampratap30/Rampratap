package com.thread;

public class ThreadExamples extends Thread{

	public void run() {
		
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		ThreadExamples t = new ThreadExamples();
		
		t.start();
		
		System.out.println("First ::");
		
		t.start();
		System.out.println("Second ::");
		

	}

}
