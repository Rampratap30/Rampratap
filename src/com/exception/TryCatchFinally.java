package com.exception;

public class TryCatchFinally {

	public static void main(String[] args) {
		try{
	        System.out.println('A');
	        try{
	            System.out.println('B');
	            throw new Exception("threw exception in B");
	        }
	        finally
	        {
	            System.out.println('X');
	        }
	        //any code here in the first try block 
	        //is unreachable if an exception occurs in the second try block
	    }
	    catch(Exception e)
	    {
	        System.out.println('Y');
	    }
	    finally
	    {
	        System.out.println('Z');
	    }

	}

}
