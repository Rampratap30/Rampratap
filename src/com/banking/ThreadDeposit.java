package com.banking;

import com.banking.Rookie_approach.BankSych;

// Class 2
// Helper class extending Thread class
public class ThreadDeposit extends Thread {

    BankSych object;
    String name;
    int dollar;

    ThreadDeposit(BankSych ob, String name, int money)
    {
        this.object = ob;
        this.name = name;
        this.dollar = money;
    }

    public void run() { object.deposit(name, dollar); }
}
