package com.leetcode.easy;

public class PalindromeNumber {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int nums = 121;
		boolean result = isPalindrome(nums);
		System.out.println(result);

	}

	private static boolean isPalindrome(int nums) {
		String orginal = String.valueOf(nums);
		String reverse = new StringBuilder(orginal).reverse().toString();
		return orginal.equals(reverse);
	}

}
