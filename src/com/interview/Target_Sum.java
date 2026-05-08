package com.interview;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public class Target_Sum {
    public static void main(String[] args) {
        int[] numbers = {12, 9, 5, 17};
        int target = 5;

//        for(int x: getSum(numbers, target)){
//            System.out.println(numbers[x]+" ");
//        }

        int result = getFindIndex(numbers, target);

        //System.out.println(result);

        List<Integer> list = Arrays.asList(1,1,2,3,4,4,5,6);

        Map<Integer, Long> map = list.stream().collect(Collectors.groupingBy(
                Function.identity(),
                Collectors.counting()
        ));

        //System.out.println(map);

        List<Integer> lists = map.entrySet().stream().filter(c->c.getValue()>1).
                map(Map.Entry::getKey).toList();

        //System.out.println(lists);


        String str ="Explaining Java occurrences";
        long count = str.chars().filter(c->c=='c').count();
        //System.out.println(count);


        String input ="arvindkumar";

        Map<Character, Long> results = input.chars().mapToObj(c->(char) c)
                .collect(Collectors.groupingBy(c->c, Collectors.counting()));


        //System.out.println(results);

        int[] numss = {2, 3, -8, 7, -1, 2, 3};

        int output = findMaxSubArray(numss);

        System.out.println(output);


    }

    private static int findMaxSubArray(int[] numss) {

        int currentSum = numss[0];
        int max = numss[0];
        for (int i = 0; i < numss.length; i++) {
           if(numss[i]> (currentSum +numss[i]))
               currentSum = numss[i];
           else
               currentSum = currentSum+numss[i];

           if(currentSum>max){
               max=currentSum;
           }
        }
        return max;
    }

    private static int getFindIndex(int[] numbers, int target) {

        if(numbers == null || numbers.length<2){
            return 0;
        }
        int temp = 0;

        for (int i = 0; i < numbers.length; i++) {
            if(numbers[i] == target){
                temp = i;
                break;
            }
        }
        return temp;
    }


    public static int [] getSum(int[] nums, int target){
        if(nums==null || nums.length<2)
            return new int[]{0,0};

        HashMap<Integer, Integer> map = new HashMap();
        for (int i = 0; i < nums.length; i++) {
            int complement = target-nums[i];
            if(map.containsKey(complement)){
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i],i);
        }
        return new int[]{};
    }

}
