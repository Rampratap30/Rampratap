package com.algorithm;

public class BinarySearch {

	public static void main(String[] args) {
		
		int arr[] = { 10, 20, 30, 40, 50 };
		int key = 30;
		int result = binarySearch(arr, key);
		if (result == -1) {
			System.out.println("Element not found in the array");
		} else {
			System.out.println("Element found at index: " + result);
		}

	}

	private static int binarySearch(int[] arr, int key) {
		int left = 0;
		int right = arr.length - 1;
		
		while (left <= right) {
			int mid = left + (right - left) / 2;
			System.out.println("Left: " + left + ", Right: " + right + ", Mid: " + mid);

			if (arr[mid] == key) {
				return mid; // Element found at index mid
			} else if (arr[mid] < key) {
				left = mid + 1; // Search in the right half
			} else {
				right = mid - 1; // Search in the left half
			}
		}
		
		
		return 0;
	}

}
