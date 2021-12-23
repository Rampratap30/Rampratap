package com.comman;

class ParentClass
{
    /*// private methods are not overridden
    private void parentMethod1()
    {
        System.out.println("Inside the parentMethod1() of ParentClass");
    }*/
    protected void parentMethod2()
    {
        System.out.println("Inside the parentMethod2() of ParentClass");
    }
}
class ChildClass extends ParentClass
{
   /* private void parentMethod1()
    {
        System.out.println("Inside the parentMethod1() of ChildClass");
    }*/
    // overriding method with more accessibility
    @Override
    public void parentMethod2()
    {
        System.out.println("Inside the parentMethod1() of ChildClass");
    }
}
public class OverridingRules {

    public static void main(String args[]) {
        ParentClass obj1 = new ParentClass();
       // obj1.parentMethod1(); //overriding private methods will give an error
        obj1.parentMethod2();

        ParentClass obj2 = new ChildClass();
        obj2.parentMethod2();


    }
}
