
public class SecondHighest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int[] array = {100,750,200,800,250};
		
		int highest = Integer.MIN_VALUE;
		
		int secondHighest = Integer.MAX_VALUE;
		
		for(int i=0;  i<array.length;i++) {
			if(array[i]>highest) {
				secondHighest = highest;
				
				highest = array[i];
			}else if(array[i] > secondHighest) {
				secondHighest = array[i];
			}
		}
		System.out.println("Highest salary :: " +highest);
		System.out.println("Second Highest salary :: " +secondHighest);
		
		

	}

}
