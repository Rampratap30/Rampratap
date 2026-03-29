package com.async.Java17;

//Only Car and Bike are allowed to extend Vehicle class
sealed class Vehicle permits Car, Bike{
    public void start(){
        System.out.println("Vehicle is starting........");
    }
}
//Permitted subclass
final class Car extends Vehicle{
    public void drive(){
        System.out.println("Car is driving........");
    }
}

//Permitted subclass
final class Bike extends Vehicle{
    public void ride(){
        System.out.println("Bike is riding.......");
    }
}

public class MainSealed {
    public static void main(String[] arg){
        Vehicle car = new Car();
        car.start(); //✅ Allowed
        ((Car) car).drive(); // ✅ Allowed

        Vehicle bike = new Bike();
        bike.start(); //✅ Allowed
        ((Bike) bike).ride(); // ✅ Allowed
    }
}




