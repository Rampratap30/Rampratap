
public class TestSumPerfect {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int [] numbers = {2,4,6,7,3,5,10};
		
		int targetVal = 10;
		
		for(int i =0; i<numbers.length;i++) {
			sumPerfect(numbers , i , numbers[i], targetVal , String.valueOf(numbers[i]));
		}

	}

	private static void sumPerfect(int[] arr, int i, int sum, int targetVal, String s) {
		// TODO Auto-generated method stub
		
		for(int j = i+1;j<arr.length;j++) {
			if(sum+arr[j]== targetVal) {
				System.out.println(s+" "+String.valueOf(arr[j]));
			}else {
				sumPerfect(arr, j, sum+arr[j], targetVal, s+" "+String.valueOf(arr[j]));
			}
		}
		
	}

}
