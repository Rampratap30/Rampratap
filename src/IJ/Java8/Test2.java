package com.async.Java8;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class Test2 {
    public static void main(String[] args) {

        BlockingQueue<Integer> q = new LinkedBlockingQueue<>(10);
        Thread producer = new Thread(new Producer(q));
        Thread consumer = new Thread(new Consumer(q));

        producer.start();
        consumer.start();
    }
}

class Producer implements Runnable {
    private BlockingQueue<Integer> queue;

    public Producer(BlockingQueue<Integer> queue){
        this.queue = queue;
    }

    @Override
    public void run(){
        int item=1;
        try {
            while(true) {
                queue.put(item);
                System.out.println("Produce: "+item);
                item++;
                Thread.sleep(2000);
            }

        } catch (Exception e) {
            // TODO: handle exception
        }
    }
}

class Consumer implements Runnable {
    private BlockingQueue<Integer> queue;

    public Consumer(BlockingQueue<Integer> queue){
        this.queue = queue;
    }

    @Override
    public void run(){
        try {
            while(true) {
                int val = queue.take();
                System.out.println("Consum: "+val);
                Thread.sleep(3000);
            }

        } catch (Exception e) {
            // TODO: handle exception
        }

    }

}
