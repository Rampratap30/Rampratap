package com.core;

class Super_1
{
  void show() { 
    System.out.println("parent class"); 
  }
}

class Sub extends Super_1
{
  void show() throws ArrayIndexOutOfBoundsException
  { 
    System.out.println("child class"); 
  }

  public static void main(String[] args)
  {
	  Super_1 s = new Sub();
	  s.show();
  }
  //Because ArrayIndexOutOfBoundsException is an unchecked exception hence, overrided show() method can throw it
}
