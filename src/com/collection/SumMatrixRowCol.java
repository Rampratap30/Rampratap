package com.collection;

public class SumMatrixRowCol {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int [][] arr = {{1,2,3},{4,5,6},{7,8,9}};
		
		int row,col,sumRow,sumCol;
		
		row = arr.length;
		
		col = arr[0].length;
		
		for(int i = 0;i<row;i++) {
			sumRow = 0;
			
			for(int j = 0;j<col;j++) {
				sumRow += arr[i][j]; 
			}
			System.out.println("Sum of "+ (i+1) +" row " +sumRow);
		}
		
		for(int i =0 ;i<col;i++) {
			sumCol = 0;
			for(int j = 0 ;j<row;j++) {
				sumCol += arr[j][i];
			}
			System.out.println("Sum of " +( i + 1) + " col " + sumCol );
		}

	}

}
