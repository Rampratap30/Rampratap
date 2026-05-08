package interview.SumTarget;

import java.util.*;

public class TripletSumProblem {
    public static void main(String[] args) {
        int[] arr = {1,2,3,4,5,6,7,8};
        int target = 10;

        List<List<Integer>> ans = TripletSumAnd(arr,target);
        for(List<Integer> tripletSum : ans){
            System.out.println(tripletSum.get(0)+" "+tripletSum.get(1)+" "+tripletSum.get(2));
        }
    }
    //Complexity is high because of 0(n4) time and O(1) Space
    private static List<List<Integer>> TripletSumAnd(int[] arr, int target) {
        List<List<Integer>> resp = new ArrayList<>();
        int n = arr.length;
        //Generating all possible triplets
        for(int i=0;i<n;i++){
            for (int j = i+1; j <n ; j++) {
                for (int k = j+1; k <n ; k++) {
                    if(arr[i]+arr[j]+arr[k]==target){
                        List<Integer> list= Arrays.asList(arr[i], arr[j], arr[k]);
                        Collections.sort(list);
                        // If triplet doesn't exist in the res, then only insert it.
                        if(!resp.contains(list)){
                            resp.add(list);
                        }
                    }
                }
            }
        }
        return resp;
    }

    //Using Hashing - O(n^2 log n) Time and O(n) Space
    /*
    The idea is to maintain a hash set to track whether a particular element occurred in the array so far or not.
    As we traverse all pairs using two nested loops, for each pair {arr[i], arr[j]},
    we check if the complement (target - arr[i] - arr[j]) is already in the set.
    If it is, we have found a triplet whose sum equals the target. Each valid triplet is inserted into ta hash set to avoid duplicates.
     */
    private static List<List<Integer>> threeSums(int[] arr, int target) {
        int n = arr.length;
        // Set to handle duplicates
        Set<List<Integer>> set = new HashSet<>();
        for (int i = 0; i < n; i++) {
            Set<Integer> s = new HashSet<>();
            for (int j=i+1;j<n;j++){
                int complement = target-arr[i]-arr[j];
                // If the complement exists in the hash set then we have found the triplet with sum, target
                if(s.contains(complement)){
                    List<Integer> curr = Arrays.asList(arr[i],arr[j],complement);
                    Collections.sort(curr);
                    set.add(curr);
                }
                s.add(arr[j]);
            }
        }
        return new ArrayList<>(set);
    }
}
