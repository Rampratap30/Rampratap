package com;

import java.util.Arrays;

public class MoveAllZeroStart {
    public static void main(String[] args) {
        // TODO Auto-generated method stub

        Integer fullArray[] = { 1, 10, 20, 0, 59, 63, 0, 88, 0 };

        for (int i = 0; i <= fullArray.length - 1; i++)  {
            if (fullArray[i] == 0 && i > 0) {
                int temp = fullArray[i - 1];
                if (temp != 0) {
                    fullArray[i - 1] = 0;
                    fullArray[i] = temp;
                    i = -1;
                }
            }
        }
       // System.out.println(Arrays.asList(fullArray).toString());


        int[] num={1,2,3,0,0,0,4,5};
        for(int i=0;i<num.length;i++){
            if(num[i]==0){
                int k=num[i];
                for(int j=0; j<=i ; j++){
                    num[j]+=k;
                    k = num[j]-k;
                    num[j]-=k;
                }
            }
        }
        for(int i = 0;i<num.length;i++)
            System.out.print(num[i]+"\t");

    }
}
