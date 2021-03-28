package com.hackerrank;

import java.util.ArrayList;
import java.util.List;

public class Solution_9 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		long [] arr = {1000000001,1000000002,1000000003,1000000004,1000000005};
		long sum=0,i;
        for(i=0;i<arr.length;i++){
            sum+=arr[(int) i];
        }
        System.out.println(sum);
		
	}

}
