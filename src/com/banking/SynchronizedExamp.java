package com.banking;

import com.banking.Rookie_approach.BankSych;

public class SynchronizedExamp {
    public static void main(String[] args) {
        // Declaring an object of Bank class and passing the
        // object along with other parameters to the
        // ThreadWithdrawal and ThreadDeposit class. This
        // will be required to call withdrawn and deposit
        // methods from those class

        // Creating object of above class inside main()
        BankSych obj = new BankSych();

        // Creating threads
        ThreadWithdrawal t1
                = new ThreadWithdrawal(obj, "Arnab", 20);
        ThreadWithdrawal t2
                = new ThreadWithdrawal(obj, "Monodwip", 40);
        ThreadDeposit t3
                = new ThreadDeposit(obj, "Mukta", 35);
        ThreadWithdrawal t4
                = new ThreadWithdrawal(obj, "Rinkel", 80);
        ThreadWithdrawal t5
                = new ThreadWithdrawal(obj, "Shubham", 40);

        // When a program calls the start() method, a new
        // thread is created and then the run() method is
        // executed
        t1.start();
        t2.start();
        t3.start();
        t4.start();
        t5.start();
    }
}

// Deposit method is called from ThreadDeposit class using
// the object of Bank class passed from the main method*/

