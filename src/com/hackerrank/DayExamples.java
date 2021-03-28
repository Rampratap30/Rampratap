package com.hackerrank;

import java.time.DayOfWeek;
import java.time.LocalDate;

public class DayExamples {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int year = 2015;
		int month = 10;
		int date = 26;
		String weekDays = null;
		LocalDate localDate = LocalDate.of(year, month, date);
		DayOfWeek dayOfWeek = localDate.getDayOfWeek();
		weekDays = dayOfWeek.toString(); 		
		System.out.println("Day ::"+weekDays);
	}
	
	

}
