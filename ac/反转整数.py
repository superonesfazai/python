# coding:utf-8

"""
给定一个 32 位有符号整数，将整数中的数字进行反转。

示例 1:
输入: 123
输出: 321

示例 2:
输入: -123
输出: -321

示例 3:
输入: 120
输出: 21

注意:
    假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−231,  231 − 1]。根据这个假设，如果反转后的整数溢出，则返回 0。
"""

class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x < pow(-2, 31) or x > pow(2, 31):
            return 0

        less_than_0 = False
        if x < 0:
            less_than_0 = True

        x = int(''.join(list(reversed((str(abs(x)))))))
        res = -1 * x if less_than_0 else x

        if res < pow(-2, 31) or res > pow(2, 31):
            return 0

        return res

_ = Solution()
# x = -0
x = 9646324351
print(_.reverse(x))