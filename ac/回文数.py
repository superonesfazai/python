# coding:utf-8

"""
判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。

eg1:
输入: 121
输出: true

eg2:
输入: -121
输出: false
解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。

eg3:
输入: 10
输出: false
解释: 从右向左读, 为 01 。因此它不是一个回文数。
"""

class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0:
            return False
        elif int(x) == 0 or x <=9:
            return True
        else:
            x = str(x)
            result = True
            for index, i in enumerate(x):
                if i == x[-index-1]:
                    pass
                else:
                    return False

        return result

_ = Solution()
x = -1
print(_.isPalindrome(x))