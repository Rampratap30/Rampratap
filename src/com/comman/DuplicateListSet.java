package com.comman;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class DuplicateListSet {

	public static void main(String[] args) {
		List<String> list=new ArrayList<String>();
        list.add("Dell");
        list.add("HP");
        list.add("Acer");
        list.add("Dell");
        list.add("HP");
        System.out.println(list);
        Set<String> set=new HashSet<String>();
        
        boolean flag = true;
        int count = 0;
        for (int i = 0; i < list.size(); i++) {
        	flag = set.add(list.get(i));
        	if(!flag) {
        		System.out.println("Duplicate value in list is = " + list.get(i));
                flag=true;
                count++;
        	}
		}
        System.out.println(count);

	}

}
