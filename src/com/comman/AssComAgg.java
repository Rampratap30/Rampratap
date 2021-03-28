package com.comman;

public class AssComAgg {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// making an engine by creating  
        // an instance of Engine class. 
        Engine engine = new Engine(); 
          
        // Making a car with engine. 
        // so we are passing a engine  
        // instance as an argument while 
        // creating instace of Car. 
        Car car = new Car(engine); 
        car.move(); 

	}

}
