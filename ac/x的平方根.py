# coding:utf-8

"""
实现 int sqrt(int x) 函数。

计算并返回 x 的平方根，其中 x 是非负整数。

由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。

eg1:
输入: 4
输出: 2

eg2:
输入: 8
输出: 2
说明: 8 的平方根是 2.82842...,
     由于返回类型是整数，小数部分将被舍去。
"""

class Solution(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        from math import sqrt

        return int(sqrt(x))

_ = Solution()
a = 8
print(_.mySqrt(a))