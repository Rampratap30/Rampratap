package com.async.algorithm.tree;

import java.util.ArrayList;

public class TreeNode {
    String data;
    ArrayList<TreeNode> childNode;

    public TreeNode(String data){
        this.data = data;
        this.childNode = new ArrayList<TreeNode>();
    }

    public void addChild(TreeNode node){
        this.childNode.add(node);
    }

    public String print(int level){
        String ret;
        ret=" ".repeat(level)+data+"\n";
        for (TreeNode node: this.childNode) {
            ret+= node.print(level+1);
        }
        return ret;
    }
}
