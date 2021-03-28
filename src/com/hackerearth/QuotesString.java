package com.hackerearth;

import java.util.Scanner;

public class QuotesString {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner sc = new Scanner(System.in);
		//System.out.println("Enter any String:");
		String name = sc.nextLine();
		//System.out.println("Before Splited: " + name);
		
		String str = escapeForJava( name, true);
		System.out.println(str);

	}
	
	public static String escapeForJava( String value, boolean quote )
	{
	    StringBuilder builder = new StringBuilder();
	    if( quote )
	        builder.append( "\"" );
	    for( char c : value.toCharArray() )
	    {
	        if( c == '\'' )
	            builder.append( "\\'" );
	        else if ( c == '\"' )
	            builder.append( "\\\"" );
	        else if( c == '\r' )
	            builder.append( "\\r" );
	        else if( c == '\n' )
	            builder.append( "\\n" );
	        else if( c == '\t' )
	            builder.append( "\\t" );
	        else if( c < 32 || c >= 127 )
	            builder.append( String.format( "\\u%04x", (int)c ) );
	        else
	            builder.append( c );
	    }
	    if( quote )
	        builder.append( "\"" );
	    return builder.toString();
	}

}

//"Trst  zsfsfs"
