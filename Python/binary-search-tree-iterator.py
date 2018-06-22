# Time:  O(1)
# Space: O(h), h is height of binary tree
#
# Implement an iterator over a binary search tree (BST).
# Your iterator will be initialized with the root node of a BST.
#
# Calling next() will return the next smallest number in the BST.
#
# Note: next() and hasNext() should run in average O(1) time
# and uses O(h) memory, where h is the height of the tree.
#


# Definition for a  binary tree node
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# USE THIS, very clean
class BSTIterator_bookshadow(object):
    def __init__(self, root):
        self.stack = []
        self.pushLeft(root)

    def pushLeft(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def hasNext(self):
        return self.stack

    def next(self):
        cur = self.stack.pop()
        self.pushLeft(cur.right)
        return cur.val

class BSTIterator(object):
    # @param root, a binary search tree's root node
    def __init__(self, root):
        self.stack = []
        self.cur = root

    # @return a boolean, whether we have a next smallest number
    def hasNext(self):
        return self.stack or self.cur

    # @return an integer, the next smallest number
    def next(self):
        while self.cur:
            self.stack.append(self.cur)
            self.cur = self.cur.left

        self.cur = self.stack.pop()
        node = self.cur
        # not clean, change to right subtree but not go deeper, but go deeper in next loop.
        self.cur = self.cur.right

        return node.val


# Time O(h) Space O(1) same algorithm as in inorder-successor-in-bst.py
class BSTIterator_ming(object):
    def __init__(self, root):
        self.root = root

        while root and root.left:
            root = root.left
        self.cur = root

    def hasNext(self):
        return self.cur

    def next(self):
        ans = self.cur.val
        if self.cur.right:
            self.cur = self.cur.right
            while self.cur.left:
                self.cur = self.cur.left
            return ans

        nextNode, r = None, self.root
        while r and r != self.cur:
            if self.cur.val < r.val:
                nextNode = r
                r = r.left
            else:
                r = r.right
        self.cur = nextNode
        return ans