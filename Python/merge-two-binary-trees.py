# Time:  O(n)
# Space: O(h)

# 617
# Given two binary trees and imagine that
# when you put one of them to cover the other,
# some nodes of the two trees are overlapped
# while the others are not.
#
# You need to merge them into a new binary tree.
# The merge rule is that if two nodes overlap,
# then sum node values up as the new value of the merged node.
# Otherwise, the NOT null node will be used as the node of new tree.
#
# Example 1:
# Input:
# 	Tree 1                     Tree 2
#           1                         2
#          / \                       / \
#         3   2                     1   3
#       /                           \   \
#       5                             4   7
# Output:
# Merged tree:
# 	     3
# 	    / \
# 	   4   5
# 	  / \   \
# 	 5   4   7
#	
# Note: The merging process must start from the root nodes of both trees.

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    # merge into the first tree and return that tree
    def mergeTrees(self, t1, t2): # pretty and clean, save a lot steps upon empty subtree
        """
        :type t1: TreeNode
        :type t2: TreeNode
        :rtype: TreeNode
        """
        if t1 and t2:
            t1.val += t2.val
            t1.left = self.mergeTrees(t1.left, t2.left)
            t1.right = self.mergeTrees(t1.right, t2.right)
            return t1
        else:
            return t1 or t2


    # if don't allow to modify input, construct a new tree
    def mergeTrees_ming(self, t1, t2): # con: construct a new tree, iterate every nodes
        if not t1 and not t2:
            return None

        v = t1.val if t1 else 0
        v += t2.val if t2 else 0
        t = TreeNode(v)
        t.left = self.mergeTrees(t1.left if t1 else None, t2.left if t2 else None)
        t.right = self.mergeTrees(t1.right if t1 else None, t2.right if t2 else None)
        return t
