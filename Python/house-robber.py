# Time:  O(n)
# Space: O(1)
#
# You are a professional robber planning to rob houses along a street.
# Each house has a certain amount of money stashed, the only constraint stopping you
# from robbing each of them is that adjacent houses have security system connected
# and it will automatically contact the police if two adjacent houses were broken into on the same night.
#
# Given a list of non-negative integers representing the amount of money of each house,
# determine the maximum amount of money you can rob tonight without alerting the police.
#
class Solution:
    # @param num, a list of integer
    # @return an integer
    def rob(self, num):
        if len(num) == 0:
            return 0

        if len(num) == 1:
            return num[0]

        num_i, num_i_1 = max(num[1], num[0]), num[0]
        for i in xrange(2, len(num)):
            num_i_1, num_i_2 = num_i, num_i_1
            num_i = max(num[i] + num_i_2, num_i_1);

        return num_i

    def rob2(self, nums): # USE THIS
        """
        :type nums: List[int]
        :rtype: int
        """
        last, now = 0, 0
        for i in nums:
            last, now = now, max(last + i, now)
        return now

    '''
    Storing both take and skip for each i is the same to the above. Proof: assume dp[i] = max(skip[i], take[i]).
    State transfer function:
       skip[i] = max(take[i-1], skip[i-1])   = dp[i-1]
       take[i] = skip[i-1]+n                 = dp[i-2]+n
    => dp[i] = max(dp[i-1], dp[i-2]+n)
    
    In fact, for each i, only the max from [take[i], skip[i]] is used to eval the later decision,
    so no need to store both take and skip for each i, only need to store the max for each i. 
    '''
    def rob_ming(self, nums):
        take, skip = 0, 0
        for n in nums:
            take, skip = skip + n, max(take, skip)
        return max(take, skip)

if __name__ == '__main__':
        print Solution().rob([8,4,8,5,9,6,5,4,4,10])
