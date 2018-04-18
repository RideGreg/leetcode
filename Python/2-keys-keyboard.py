# Time:  O(sqrt(n))
# Space: O(1)

# Initially on a notepad only one character 'A' is present.
# You can perform two operations on this notepad for each step:
#
# Copy All: You can copy all the characters present on the notepad
# (partial copy is not allowed).
# Paste: You can paste the characters which are copied last time.
# Given a number n.
# You have to get exactly n 'A' on the notepad by performing the minimum
#  number of steps permitted.
# Output the minimum number of steps to get n 'A'.
#
# Example 1:
# Input: 3
# Output: 3
# Explanation:
# Intitally, we have one character 'A'.
# In step 1, we use Copy All operation.
# In step 2, we use Paste operation to get 'AA'.
# In step 3, we use Paste operation to get 'AAA'.
# Note:
# The n will be in the range [1, 1000].


class Solution(object):
    def minSteps(self, n):
        """
        :type n: int
        :rtype: int
        """
        result = 0
        p = 2
        # the answer is the sum of prime factors
        # f(x) = f(x/2) + f(2), f(x) = f(x/3) + f(3) ...
        while p**2 <= n:
            while n % p == 0: # a factor
                result += p
                n //= p # floor/integer division, also ok to use true division
            p += 1
        if n > 1:
            result += n
        return result

print Solution().minSteps(9)
print Solution().minSteps(10)
print Solution().minSteps(11)
print Solution().minSteps(12)
print Solution().minSteps(71)
