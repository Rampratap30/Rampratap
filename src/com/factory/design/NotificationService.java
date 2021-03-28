package com.factory.design;

public class NotificationService {

	//ResourceBundle uses factory method design pattern.
	//factory method in the interface lets a class defer the instantiation to one or more concrete subclasses.
	public static void main(String[] args) {
		NotificationFactory notificationFactory = new NotificationFactory();
		Notification notification  = notificationFactory.createNotification("EMAIL");
		notification.notifyUser();
	}
}
