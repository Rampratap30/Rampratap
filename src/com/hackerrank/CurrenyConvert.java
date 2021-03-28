package com.hackerrank;

import java.text.NumberFormat;
import java.util.Locale;
import java.util.Scanner;

public class CurrenyConvert {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scanner = new Scanner(System.in);
        double payment = scanner.nextDouble();
        scanner.close();

        // Write your code here.
        NumberFormat currencyUs = NumberFormat.getCurrencyInstance();
        String us = currencyUs.format(payment);
        NumberFormat currencyINR = NumberFormat.getCurrencyInstance(new Locale("en","in"));
        String india = currencyINR.format(payment);
        
        NumberFormat currencyChin = NumberFormat.getCurrencyInstance(Locale.CHINA);
        String china = currencyChin.format(payment);
        
        NumberFormat currencyFran = NumberFormat.getCurrencyInstance(Locale.FRANCE);
        String france = currencyFran.format(payment);
        
        
        System.out.println("US: " + us);
        System.out.println("India: " + india);
        System.out.println("China: " + china);
        System.out.println("France: " + france);

	}

}
