package com.async.Java8;


import java.util.concurrent.atomic.AtomicInteger;

public class Test_Thread {
    public static void main(String[] args) throws InterruptedException {
        Counter c = new Counter();

        //Thread 1 increment count 1000 times
        Thread t1 = new Thread(()->{
            for (int i = 0; i < 1000 ; i++)
                c.increment();
        });

        //Thread 2 increment count 1000 times
        Thread t2= new Thread(() ->{
            for (int i = 0; i < 1000; i++) c.increment();
        });


        //Start Thread 1
        t1.start();

        //Start Thread2
        t2.start();

        //Wait for Thread 1 to finish
        t1.join();

        //Wait for Thread 2 to finish
        t2.join();

        // May be < 2000 due to race condition
        System.out.println("Final Count: " + c.count);
    }
}

class Counter{
    /*int count = 0;
    void increment(){
        count++;
    }*/

    AtomicInteger count = new AtomicInteger(0);

    void increment(){
        count.getAndIncrement();
    }
}


