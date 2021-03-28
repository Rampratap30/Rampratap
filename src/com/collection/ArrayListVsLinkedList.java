package com.collection;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;


public class ArrayListVsLinkedList {

	private static final int MAX = 500000;
	static String[] strings = maxArray();
	public static void main(String[] args) {
		
		//linkedListAll();
	}
	class Watch {
        private long startTime;
        private long endTime;

        public void start() {
            startTime = System.nanoTime();
        }

        private void stop() {
            endTime = System.nanoTime();
        }

        public void totalTime(String s) {
            stop();
            System.out.println(s + (endTime - startTime));
        }
    }
	private static String[] maxArray() {
		String[] strings = new String[MAX];
		Boolean result = Boolean.TRUE;
		for (int i = 0; i < MAX; i++) {
			strings[i] = getString(result, i);
			result = !result;
		}
		return strings;
	}

	private static String getString(Boolean result, int i) {
		return String.valueOf(result) + i + String.valueOf(!result);
	}
	
	public void arrayListAll() {
		Watch watch = new Watch();
		List<String> stringList = Arrays.asList(strings);
        List<String> arrayList = new ArrayList<String>(MAX);
        
        watch.start();
        arrayList.addAll(stringList);
        watch.totalTime("Array List addAll() = ");
	}
	
	public  void linkedListAll() {
		Watch watch = new Watch();
		List<String> stringList = Arrays.asList(strings);
        
        watch.start();
        List<String> linkedList = new LinkedList<String>();
        linkedList.addAll(stringList);
        watch.totalTime("Linked List addAll() = ");
	}

}


