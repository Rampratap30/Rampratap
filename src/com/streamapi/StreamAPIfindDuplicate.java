package com.streamapi;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import java.util.stream.Collectors;

public class StreamAPIfindDuplicate {
	
	static boolean isOk;

	public static void main(String[] args) throws ParseException {
		 // Initial stream 
        List<Integer> list 
            = Arrays.asList(5, 13, 4, 21, 13, 27,4, 59, 59, 34);
        
		/*
		 * List<Integer> distintList =
		 * list.stream().distinct().collect(Collectors.toList());
		 * 
		 * int count = list.size()-distintList.size();
		 * 
		 * System.out.println(count);
		 */
        
        Set<Integer> set = new HashSet<Integer>(list);
        
        int count = list.size() - set.size();
        
        //System.out.println(count);
        
        List<String> lists = Arrays.asList("Ram", "Test", "Ram", "Sohita");
        
        List<String> removeList = lists.stream().distinct().collect(Collectors.toList());
        
        //System.out.println(removeList);
        
        System.out.println(isOk);
        int x = 3;
        int y = 5;
        int z = 10;
        System.out.println(++z + y - y + z +x++);
        
        //25
        
        TreeSet t = new TreeSet();
        t.add("13");
        t.add("11");
        t.add("20");
        System.out.println(t);
        
        float f = 1F;
        SimpleDateFormat sdf = new SimpleDateFormat("dd-M-yyyy hh:mm:sss");
        String dateInString = "06-06-1991 19:20:000";
        Date date = sdf.parse(dateInString);
        
        System.out.println(date);
        
        //add size with out collection
        
        int[] intA = new int[10];
        int[] temp = new int[intA.length+5];
        
        for(int i = 0; i < intA.length ; i++){
        	temp[i] = intA[i];
        }
        intA = temp;
        
        System.out.println(intA.length);
        

	}

}
