package com.datastructures.binarySearchTree;

public class Main {
    public static void main(String[] args) {
        BinarySearchTree myBinarySearchTree = new BinarySearchTree();


        myBinarySearchTree.insert(47);
        myBinarySearchTree.insert(21);
        myBinarySearchTree.insert(76);
        myBinarySearchTree.insert(18);
        myBinarySearchTree.insert(52);
        myBinarySearchTree.insert(82);

        myBinarySearchTree.insert(27);

        System.out.println(myBinarySearchTree.root.left.right.value);
    }
}
