package interview.SumTarget;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class TripletSumNotTarget {
    public static void main(String[] args) {
        int[] nums ={-1,0,1,2,-1,-4};
        List<List<Integer>> anss = TripletSum(nums);
        for(List<Integer> tripletSum : anss){
            System.out.println(tripletSum.get(0)+" "+tripletSum.get(1)+" "+tripletSum.get(2));
        }
    }

    //Complexity is high because of 0(n4) time and O(1) Space
    private static List<List<Integer>> TripletSum(int[] nums) {
        List<List<Integer>> resp = new ArrayList<>();
        int n = nums.length;
        //Generating all possible triplets
        for (int i = 0; i < n; i++) {
            for (int j = i+1; j <n ; j++) {
                for (int k = j+1; k < n; k++) {
                    if(nums[i]+nums[j]+nums[k]==0){
                        List<Integer> curr = Arrays.asList(nums[i], nums[j], nums[k]);
                        Collections.sort(curr);
                        if(!resp.contains(curr)){
                            resp.add(curr);
                        }
                    }
                }
            }
        }
        return resp;
    }
}
