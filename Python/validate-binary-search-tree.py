# Time:  O(n)
# Space: O(1)
#
# Given a binary tree, determine if it is a valid binary search tree (BST).
#
# Assume a BST is defined as follows:
#
# The left subtree of a node contains only nodes with keys less than the node's key.
# The right subtree of a node contains only nodes with keys greater than the node's key.
# Both the left and right subtrees must also be binary search trees.
#

# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# Morris Traversal Solution
class Solution:
    # @param root, a tree node
    # @return a list of integers
    def isValidBST(self, root):
        prev, cur = None, root
        while cur:
            if cur.left is None:
                if prev and prev.val >= cur.val:
                    return False
                prev = cur
                cur = cur.right
            else:
                node = cur.left
                while node.right and node.right != cur:
                    node = node.right

                if node.right is None:
                    node.right = cur
                    cur = cur.left
                else:
                    if prev and prev.val >= cur.val:
                        return False
                    node.right = None
                    prev = cur
                    cur = cur.right

        return True


# Time:  O(n)
# Space: O(h)
class Solution2:
    # @param root, a tree node
    # @return a boolean
    def isValidBST(self, root):
        def validate(root, low, high):
            if root is None:
                return True
            return low < root.val < high \
                   and validate(root.left, low, root.val) \
                   and validate(root.right, root.val, high)

        return validate(root, float("-inf"), float("inf"))

    def isValidBST_simpleIteratpreion(self, root):
        prev, stk = float("-inf"), [(root, False)]

        while stk:
            cur, visited = stk.pop()
            if cur:
                if not visited:
                    stk.append((cur.right, False))
                    stk.append((cur, True))
                    stk.append((cur.left, False))
                else:
                    if prev >= cur.val: return False
                    prev = cur.val
        return True

    def isValidBST_simpleRecursion(self, root):
        def inOrder(root):
            if root:
                if not inOrder(root.left):
                    return False
                if prev[0] >= root.val:
                    return False
                prev[0] = root.val
                if not inOrder(root.right):
                    return False
            return True
        prev = [float('-inf')]
        return inOrder(root)

if __name__ == "__main__":
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)
    print(Solution().isValidBST(root))
