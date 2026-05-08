package interview.SumTarget;

import java.util.*;

public class FourNumProblem {
    public static void main(String[] args) {
        int[] arr = {2,2,2,2,2};
        int target = 8;

        List<List<Integer>> ans = fourSum(arr,target);
        for(List<Integer> fourSum : ans){
            System.out.println(fourSum.get(0)+" "+fourSum.get(1)+" "+fourSum.get(2)+" "+fourSum.get(3));
        }
    }

    private static List<List<Integer>> fourSumAnd(int[] arr, int target) {
        List<List<Integer>> resp = new ArrayList<>();
        int n = arr.length;

        for(int i=0;i<n;i++){
            for (int j = i+1; j <n ; j++) {
                for (int k = j+1; k < n; k++) {
                    for (int l = k+1; l <n ; l++) {
                        if(arr[i]+arr[j]+arr[k]+arr[l]==target){
                            List<Integer> curr = Arrays.asList(arr[i],arr[j],arr[k],arr[l]);
                            Collections.sort(curr);
                            // If four doesn't exist in the res, then only insert it.
                            if(!resp.contains(curr)){
                                resp.add(curr);
                            }
                        }
                    }
                }
            }
        }
        return resp;
    }

    public static List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        int n = nums.length;

        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i-1]) continue; // skip duplicates
            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j-1]) continue;
                int left = j + 1, right = n - 1;
                while (left < right) {
                    long sum = (long) nums[i] + nums[j] + nums[left] + nums[right];
                    if (sum == target) {
                        res.add(Arrays.asList(nums[i], nums[j], nums[left], nums[right]));
                        while (left < right && nums[left] == nums[left+1]) left++;
                        while (left < right && nums[right] == nums[right-1]) right--;
                        left++; right--;
                    } else if (sum < target) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        return res;
    }
}
