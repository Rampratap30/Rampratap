package interview.SumTarget;

import java.util.HashMap;

public class TwoNumProblem {
    public static void main(String[] args) {
        int[] arr= {2,7,11,15};
        int target = 9;
        int [] resp = twoNums(arr, target);
        for (int i = 0; i < resp.length; i++) {
            System.out.print(i+" ");
        }
    }

    private static int[] twoNums(int[] nums,int target){
        if(nums == null || nums.length<2 )
            return new int[] {0,0};

        HashMap<Integer, Integer> map=new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            if(map.containsKey(nums[i])){
                return new int[]{map.get(nums[i]),i};
            }else{
                map.put(target-nums[i],i);
            }
        }
        return new int[]{0,0};
    }
}
