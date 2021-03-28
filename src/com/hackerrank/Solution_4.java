package com.hackerrank;

import java.util.Scanner;

public class Solution_4 {

	public static void main(String[] args) {
		
		Scanner sc = new Scanner(System.in);
        int t=sc.nextInt();

        for(int i=0;i<t;i++)
        {

            try
            {
                long x=sc.nextLong();
                System.out.println(x+" can be fitted in:");
                if(x>=-32768 && x<=32767)System.out.println("* short");
                if(x>=-2147483648 && x<= 2147483647)System.out.println("* int");                
                System.out.println("* long");
                //Complete the code
            }
            catch(Exception e)
            {
                System.out.println(sc.next()+" can't be fitted anywhere.");
            }

        }

	}

}
