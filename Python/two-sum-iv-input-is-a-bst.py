
# Time:  O(n)
# Space: O(h)

# 653
# Given a Binary Search Tree and a target number,
# return true if there exist two elements in the BST such that their sum is equal to the given target.
#
# Example 1:
# Input:
#     5
#    / \
#   3   6
#  / \   \
# 2   4   7
#
# Target = 9
#
# Output: True
# Example 2:
# Input:
#     5
#    / \
#   3   6
#  / \   \
# 2   4   7
#
# Target = 28
#
# Output: False

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    # "yield from subgenerator()" == "for i in subgenerator(): yield i"
    # http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html
    def findTarget(self, root, k): # USE THIS, BST, save space
        def left_generator(node):
            if node.left: yield from left_generator(node.left)
            yield node.val
            if node.right: yield from left_generator(node.right)

        def right_generator(node):
            if node.right: yield from right_generator(node.right)
            yield node.val
            if node.left: yield from right_generator(node.left)

        lGen, rGen = left_generator(root), right_generator(root)
        lv, rv = next(lGen), next(rGen)
        while lv < rv:
            if lv + rv < k:
                lv = next(lGen)
            elif lv + rv > k:
                rv = next(rGen)
            else:
                return True
        return False

    def findTarget4(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: bool
        """
        class BSTIterator(object):
            def __init__(self, root, forward):
                self.__node = root
                self.__forward = forward
                self.__s = []
                self.__cur = None
                self.next()

            def val(self):
                return self.__cur

            def next(self):
                while self.__node or self.__s:
                    if self.__node:
                        self.__s.append(self.__node)
                        self.__node = self.__node.left if self.__forward else self.__node.right
                    else:
                        self.__node = self.__s.pop()
                        self.__cur = self.__node.val
                        self.__node = self.__node.right if self.__forward else self.__node.left
                        break


        if not root:
            return False
        left, right = BSTIterator(root, True), BSTIterator(root, False)
        while left.val() < right.val():
            if left.val() + right.val() == k:
                return True
            elif left.val() + right.val() < k:
                left.next()
            else:
                right.next()
        return False

    # Time O(n) Space (n)
    def findTarget2(self, root, k): # DFS+hash, avoid nest exceed limit
        stack, seen = [root], set()
        while stack:
            curr = stack.pop()
            if k - curr.val in seen:
                return True
            seen.add(curr.val)

            if curr.left:
                stack.append(curr.left)
            if curr.right:
                stack.append(curr.right)
        return False

    def findTarget3(self, root, k):
        def preOrder(root):
            if not root: return False
            if k-root.val in ht:
                return True
            ht.add(root.val)
            return preOrder(root.left) or preOrder(root.right)

        ht = set()
        return preOrder(root)

root = TreeNode(5)
root.left, root.right = TreeNode(3), TreeNode(6)
root.left.left, root.left.right = TreeNode(2), TreeNode(4)
root.right.right = TreeNode(7)
print(Solution().findTarget(root, 9))