package com.comman;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DuplicateKeyValue {

	public static void main(String[] args) {
		 List<String> list = new ArrayList<String>();
	      list.add("Ashok");
	      list.add("Vinod");
	      list.add("Kumar");
	      list.add("Ashok");
	      list.add("Mariyala");
	      list.add("Venkata");
	      list.add("Mariyala");
	      list.add("Vinod");
	      list.add("Ashok");
	      list.add("Kumar");
	      
	      Map<String,Integer> duplicates = new HashMap<String, Integer>();
	      
	      for (String str : list) {
			
	    	  if(duplicates.containsKey(str)) {
	    		  duplicates.put(str, duplicates.get(str)+1); 
	    	  }else {
	    		  duplicates.put(str,1);
	    	  }
		}
	    for (Map.Entry<String, Integer> entry : duplicates.entrySet()) {
	    	System.out.println(entry.getKey() + " = " + entry.getValue());			
		}
	      

	}

}
