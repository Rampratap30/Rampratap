package interview.sum;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class TripletSum {
    public static void main(String[] args) {
        int[] arr = {-1,0,1,2,-1,-4};
        List<List<Integer>> ans = tripletSum(arr);
        for(List<Integer> triplet: ans){
            System.out.println(triplet.get(0)+" "+triplet.get(1)+" "+triplet.get(2));
        }
    }

    private static List<List<Integer>> tripletSum(int[] nums){
        List<List<Integer>> resp = new ArrayList<>();
        // 1. Sort the array to use two-pointer technique and skip duplicates
        Arrays.sort(nums);

        for (int i = 0; i < nums.length-2; i++) {
            // 3. Skip duplicate elements for the first position
            if(i >0 && nums[i]==nums[i-1]) continue;//skip duplicate
            int left = i+1, right = nums.length-1;
            while(left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    resp.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    // 4. Move pointers and skip duplicates for second/third positions
                    while (left < right && nums[left] == nums[left + 1]) left ++;//skip
                    while (left < right && nums[right] == nums[right - 1]) right--;//skip
                    left++;
                    right--;
                } else if (sum < 0) {
                    // Sum too small, move left pointer to increase it
                    left++;
                }else {
                    // Sum too large, move right pointer to decrease it
                    right--;
                }
            }
        }
        return resp;
    }
}
