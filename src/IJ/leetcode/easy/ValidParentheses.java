package com.async.leetcode.easy;

import java.util.Stack;

public class ValidParentheses {
    public static void main(String[] args) {
        String str="{}";

        boolean result = isValid(str);
        System.out.println(result);
    }

    public static boolean isValid(String str){
        Stack<Character> stack = new Stack<>();
        for(char c : str.toCharArray()){
            if(c =='('|| c=='{' ||c=='['){
                stack.push(c);
            }else{
                if (stack.isEmpty())return false;
                char open = stack.pop();
                if(c==')' && open !='(') return false;
                if(c=='}' && open !='{') return false;
                if(c==']' && open !='[') return false;
            }
        }
        return stack.isEmpty();
    }
}
