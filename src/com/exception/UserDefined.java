package com.exception;

public class UserDefined extends Exception {
	private static int accno[] = {1001,1002,1003,1004,1005};

	private static String name[] = {"raju","ramu","gopi","baby","bunny"};

	private static double bal[] = {9000.00,5675.27,3000.00,1999.00,1600.00};
	UserDefined(){}
	UserDefined(String str){
	    super(str);
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		try {
	        //System.exit(0); -------------LINE 1---------------------------------
	        System.out.println("accno"+"\t"+"name"+"\t"+"balance");
	        for (int i = 0; i < 5; i++) {
	            System.out.println(accno[i]+"\t"+name[i]+"\t"+bal[i]);
	            if (bal[i] < 1700) {
	            	UserDefined ue = new UserDefined("Balance amount Less");
	                throw ue;
	            }//end if
	        }
		}//end try
	    catch (UserDefined ue)
	    {
	        System.out.println(ue);
	    }
	    finally{
	        System.out.println("Finnaly");
	        System.out.println("Finnaly");
	        System.out.println("Finnaly");
	    }

	}

}
