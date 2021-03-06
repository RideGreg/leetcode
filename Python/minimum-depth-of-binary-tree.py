# Time:  O(n)
# Space: O(h), h is height of binary tree, avg h = logn, worst h = n
# 111
# Given a binary tree, find its minimum depth.
#
# The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
#

# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    # @param root, a tree node
    # @return an integer
    def minDepth(self, root): # USE THIS, don't need finish all nodes
        if not root: return 0
        import collections
        queue = collections.deque([(root, 1)])
        while queue:
            node, step = queue.popleft()
            if not node.left and not node.right:
                return step
            if node.left:
                queue.append((node.left, step + 1))
            if node.right:
                queue.append((node.right, step + 1))


    def minDepth_dfs(self, root):
        if root is None:
            return 0

        if root.left and root.right:
            return min(self.minDepth(root.left), self.minDepth(root.right)) + 1
        else:
            return max(self.minDepth(root.left), self.minDepth(root.right)) + 1


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    print Solution().minDepth(root)
