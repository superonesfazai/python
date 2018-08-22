# coding:utf-8

"""
给定一个由整数组成的非空数组所表示的非负整数，在该数的基础上加一。

最高位数字存放在数组的首位， 数组中每个元素只存储一个数字。

你可以假设除了整数 0 之外，这个整数不会以零开头。

eg1:
输入: [1,2,3]
输出: [1,2,4]
解释: 输入数组表示数字 123。

eg2:
输入: [4,3,2,1]
输出: [4,3,2,2]
解释: 输入数组表示数字 4321。
"""

class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        sum = 0
        a_len = len(digits)
        for index, item in enumerate(digits):
            sum += item * pow(10, a_len-1)
            a_len -= 1

        sum += 1
        result = []
        # print(sum)
        for i in str(sum):
            result.append(int(i))

        return result

_ = Solution()
# a = [1, 2, 3]
# a = [9, 9, 9]
a = [4,3,2,1]
print(_.plusOne(a))