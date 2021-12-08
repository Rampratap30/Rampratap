
public class AllZeroShift {

	public static void main(String[] args) {
		int arr[] = { 0, 1, 9, 8, 4, 0, 0, 2, 7, 0, 6, 0, 9 };
		int n = arr.length;

		
		/*
		 * System.out.print("Original array: "); printArray(arr, n);
		 */
	    
	    moveZerosToEnd(arr,  n);

		for (int i = 0; i < n; i++)
			System.out.print(arr[i] + " ");
	    //System.out.print("\nModifed array: ");
	    //printArray(arr, n);
		
	}
	
	// function to print the array elements 
	/*static void printArray(int arr[], int n) {
	    for (int i = 0; i < n; i++) 
	    System.out.print(arr[i] + " "); 
	}*/
	
	// the end of array 
	static void moveZerosToEnd(int arr[], int n) { 
	      
	    // Count of non-zero elements 
	    int count = 0; 
	    int temp; 
	  
	    // Traverse the array. If arr[i] is  
	    // non-zero, then swap the element at  
	    // index 'count' with the element at  
	    // index 'i' 
	    for (int i = 0; i < n; i++) { 
	    if (arr[i] != 0) {
	        temp = arr[count]; 
	        arr[count] = arr[i]; 
	        arr[i] = temp; 
	        count++;
	    }
			//System.out.print(arr[i] + " ");
	    }

	} 

}
