package com.comman;

public final class Car {
	
	// For a car to move,  
    // it need to have a engine. 
    //private final Engine engine; // Composition 
    private Engine engine;     // Aggregation
	
	
	Car(Engine engine) 
    { 
        this.engine = engine; 
    }
	
	public void move()  
    { 
          
        if(engine != null) 
        { 
            engine.work(); 
            System.out.println("Car is moving "); 
        } 
    } 
}
