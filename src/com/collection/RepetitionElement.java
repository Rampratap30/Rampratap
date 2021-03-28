package com.collection;

public class RepetitionElement {
	
	static int arr [] = {1,5,6};
	
	static int wayCount(int N) {
		
		int count[] = new int[N+1]; //8
		
		count[0] = 1;  // 1
		
		// looping 0 to 7 
		for(int i = 0; i <= N ;i++) {
			
			// looping 0 to 2 length 
			for(int j = 0 ; j<arr.length;j++)
			{	
				
				// i less then and equals arr[1,5,6]
				if(i>=arr[j]) {
					
					//
					count[i] += count[i-arr[j]];		
					
				}
				
			}
			
		}
		return count[N];
		
	}
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int N = 7;
		
		System.out.println("Total number of ways ::" +wayCount(N));

	}

}
