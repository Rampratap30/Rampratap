package com.comman;

class A{
    void msg(){
        System.out.println("Hello");
    }
}
class B {
    void msg(){
        System.out.println("Welcome");
    }
}

class NotSupportMultipleInheritance extends A{ // extends A,B cannot support multiple classes so does not support multiple inheritance

    public static void main(String args[]){

    }
}
