# coding:utf-8


"""
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

注意：给定 n 是一个正整数。

eg1:
输入： 2
输出： 2
解释： 有两种方法可以爬到楼顶。
1.  1 阶 + 1 阶
2.  2 阶

eg2:
输入： 3
输出： 3
解释： 有三种方法可以爬到楼顶。
1.  1 阶 + 1 阶 + 1 阶
2.  1 阶 + 2 阶
3.  2 阶 + 1 阶
"""

class Solution(object):
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        condition = [0] * (n + 1)
        condition[0] = 1
        condition[1] = 1
        for i in range(2, n + 1):
            condition[i] = condition[i-1] + condition[i-2]

        return condition[n]

'''
分析:
4
1111
112
22
211
121

5
11111
1112
1121
1211
2111
122
212
221
'''

_ = Solution()
n = 4
print(_.climbStairs(n))
