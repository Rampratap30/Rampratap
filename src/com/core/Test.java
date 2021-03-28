package com.core;

import java.util.Properties;

public class Test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Properties p = System.getProperties();
		p.setProperty("pirate", "scurvy");
		String s = p.getProperty("argProp") +"";
		s += p.getProperty("pirate");
		System.out.println(s);
	}

}
