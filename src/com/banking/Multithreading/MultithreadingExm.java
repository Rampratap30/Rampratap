package com.banking.Multithreading;

import com.banking.Rookie_approach.Bank;

public class MultithreadingExm {
    public static void main(String[] args) {
        // Declaring an object of Bank class and passing the
        // object along with other parameters to the
        // ThreadWithdrawal and ThreadDeposit class. This
        // will be required to call withdrawn and deposit
        // methods from those class

        // Creating an object of class1
        Bank obj= new Bank();

        ThreadWithdrawal t1 = new ThreadWithdrawal(obj, "Arnab", 20);
        ThreadWithdrawal t2 = new ThreadWithdrawal(obj, "Monodwip", 40);
        ThreadDeposit t3 = new ThreadDeposit(obj, "Mukta", 35);
        ThreadWithdrawal t4 = new ThreadWithdrawal(obj, "Rinkel", 80);
        ThreadWithdrawal t5 = new ThreadWithdrawal(obj, "Shubham", 40);

        // When a program calls the start() method, a new
        // thread is created and then the run() method is
        // executed.

        // Starting threads created above
        t1.start();
        t2.start();
        t3.start();
        t4.start();
        t5.start();


    }
}

//------------------- Multithreading Process ------------------------------------
// Method - Withdraw method
// Called from ThreadWithdrawal class
// using the object of Bank class passed
// from the main() method
class ThreadWithdrawal extends Thread {

    Bank object;
    String name;
    int dollar;

    // Constructor of this method
    ThreadWithdrawal(Bank ob, String name, int money)
    {
        this.object = ob;
        this.name = name;
        this.dollar = money;
    }

    // run() method for thread
    public void run() { object.withdrawn(name, dollar); }
}
// Deposit method is called from ThreadDeposit class
// using the object of Bank class passed
// from the main method
class ThreadDeposit extends Thread {

    Bank object;
    String name;
    int dollar;
    ThreadDeposit(Bank ob, String name, int money)
    {
        // This keyword refers t ocurrent instance itself
        this.object = ob;
        this.name = name;
        this.dollar = money;
    }

    public void run() { object.deposit(name, dollar); }
}
