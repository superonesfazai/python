# coding:utf-8

"""
给定一个非负整数 num，反复将各个位上的数字相加，直到结果为一位数

eg:
输入: 38
输出: 2
解释: 各位相加的过程为：3 + 8 = 11, 1 + 1 = 2。 由于 2 是一位数，所以返回 2。
"""

class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """
        if len(str(num)) == 1:
            return int(num)

        num_list = [int(i) for i in str(num)]
        sum = 0
        for i in num_list:
            sum += i
        # print(sum)

        return self.addDigits(sum)

_ = Solution()
a = 101
print(_.addDigits(a))