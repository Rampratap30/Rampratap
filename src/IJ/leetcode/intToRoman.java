package com.async.leetcode;

import java.util.List;

/*
Input: num = 3749

Output: "MMMDCCXLIX"

Explanation:

3000 = MMM as 1000 (M) + 1000 (M) + 1000 (M)
 700 = DCC as 500 (D) + 100 (C) + 100 (C)
  40 = XL as 10 (X) less of 50 (L)
   9 = IX as 1 (I) less of 10 (X)
Note: 49 is not 1 (I) less of 50 (L) because the conversion is based on decimal places

Symbol	Value
I	1
V	5
X	10
L	50
C	100
D	500
M	1000
*/
public class intToRoman {
    public static void main(String[] args) {
       int inputNumber=54;
       String result = intToRoman(inputNumber);
       System.out.println("Input Number " + inputNumber +"intToRoman Result::--->"+result);
    }

    public static String intToRoman(int num) {
        List<String> cs
                = List.of("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I");
        List<Integer> vs = List.of(1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1);
        StringBuilder ans = new StringBuilder();
        for (int i = 0, n = cs.size(); i < n; ++i) {
            while (num >= vs.get(i)) {
                num -= vs.get(i);
                ans.append(cs.get(i));
            }
        }
        return ans.toString();
    }
}
