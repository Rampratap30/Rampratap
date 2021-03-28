package com.streamapi;

import java.util.Arrays;
import java.util.HashSet;

public class FindUniqueWords {

	public static void main(String[] args) {
		
		String str = "apple banana mango grape lichi mango apple grape";
        
        String[] words = str.split(" ");
         
        HashSet<String> uniqueWords = new HashSet<String>(Arrays.asList(words));
        
        System.out.println(uniqueWords.size());
         //int count =  0;
        for(String s:uniqueWords)        	
            System.out.println(s);
        	//count++;

	}

}
