
public class TestSum {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int[] arry = {0,9,3,6,2,2,12};//{2,3,4,6,1};
		
		int target = 9;
		
		for(int i = 0;i<arry.length;i++) {
			sumTest(arry,i, arry[i], target, String.valueOf(arry[i]));
		}
	}

	static void sumTest(int[] arry, int i, int sum, int target, String s) {
		
		for(int j = i+1;j<arry.length;j++) {
			if(sum+arry[j] == target) {
				System.out.println(s +" "+String.valueOf(arry[j]));	
			}else {
				sumTest(arry,j,sum+arry[j],target,s+" "+String.valueOf(arry[j]));
			}
		}
		// TODO Auto-generated method stub
		
	}

}
