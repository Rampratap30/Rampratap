package com.morgan;

public class User {
    String name;
    boolean isActive;

    User(String name,boolean isActive){
        this.name = name;
        this.isActive = isActive;
    }

    public String getName(){
        return name;
    }

    public boolean isActive(){
        return isActive;
    }
}
