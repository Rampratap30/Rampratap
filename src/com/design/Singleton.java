package com.design;

//Lazy loading
public class Singleton {
	
	/*
	 * private static Singleton instance;
	 * 
	 * public String value;
	 * 
	 * private Singleton(String value) { try { Thread.sleep(1000); } catch
	 * (InterruptedException e) { // TODO Auto-generated catch block
	 * e.printStackTrace(); } this.value = value; }
	 * 
	 * public static Singleton getSingleton(String value) { if(instance == null) {
	 * instance = new Singleton(value); } return instance; }
	 */
	
	
	//double checking locking
	
	private static volatile Singleton _instance;
	
	public String value;
	private Singleton(String value) {
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		this.value = value;
	}
	
	public static Singleton getSingleton(String value) {
		
		if(_instance ==null) {
			synchronized (Singleton.class) {
				_instance = new Singleton(value);				
			}
		}
		
		return _instance;
		
	}
	
	

}
