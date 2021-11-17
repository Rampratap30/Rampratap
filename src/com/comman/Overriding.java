package com.comman;

class Shape{
    void draw(){
        System.out.println("Inside the method of Parent class ");
        System.out.println("Drawing Shapes");
    }
}
class Circle extends Shape{
    @Override
    void draw() {
        System.out.println("Inside the overridden method of the child class ");
        System.out.println("Drawing Circle");
    }
}
public class Overriding {

    public static void main(String args[])
    {
        Shape obj = new Shape();
        obj.draw();

        Shape obj1 = new Circle();
        obj1.draw();
    }
}
