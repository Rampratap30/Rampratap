package com.hackerearth;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class CaseConvertion {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter wr = new PrintWriter(System.out);
        int T = Integer.parseInt(br.readLine().trim());
        for(int t_i=0; t_i<T; t_i++)
        {
            String s = br.readLine();

            String out_ = caseConversion(s);
            System.out.println(out_);
            System.out.print("");
         }

         wr.close();
         br.close();

	}
	
	 static String caseConversion(String value){
		
		final char[] name = value.toCharArray();
		final StringBuilder builder = new StringBuilder();

		for (int i = 0; i < name.length; i++) {
			if (Character.isUpperCase(name[i]) || name[i] == '.' || name[i] == '$') {
				if (i != 0 && name[i - 1] != '.' && name[i - 1] != '$') {
					builder.append('_');
				}
				if (name[i] != '.' && name[i] != '$') {
					builder.append(Character.toLowerCase(name[i]));
				}
			} else {
				builder.append(name[i]);
			}
		}

		return builder.toString();
		 
		 
		/*
		 * String ret = value.replaceAll("([A-Z]+)([A-Z][a-z])",
		 * "$1_$2").replaceAll("([a-z])([A-Z])", "$1_$2"); return ret.toLowerCase();
		 */
	 }

}
/*
 * Input
6
HackerEarth
primeCheck
OddOrEven
random
getRandom
macOS
Your Code's Output

hacker_earth
prime_check
odd_or_even
random
get_random
mac_o_s
 */
