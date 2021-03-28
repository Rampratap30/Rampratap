package com.collection;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class ReadAndWriteTxt {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		File file = new File("D://doc//input.txt"); 
		  
		  BufferedReader br = new BufferedReader(new FileReader(file)); 
		  
		  StringBuilder sb = new StringBuilder();
		  String st; 
		  while ((st = br.readLine()) != null) 
		    System.out.println(st); 
		  
		 
		 
		  	
		  	
		  	
		  } 

	}

