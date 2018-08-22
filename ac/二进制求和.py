# coding:utf-8

"""
给定两个二进制字符串，返回他们的和（用二进制表示）。

输入为非空字符串且只包含数字 1 和 0。

eg1:
输入: a = "11", b = "1"
输出: "100"

eg2:
输入: a = "1010", b = "1011"
输出: "10101"
"""

class Solution(object):
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        index1, index2 = len(a) - 1, len(b) - 1
        result = ""
        # 进位的值，0表示不进位（进位0），1表示进位1
        add1 = 0
        while index1 >= 0 or index2 >= 0:
            t1 = int(a[index1]) if index1 >= 0 else 0
            t2 = int(b[index2]) if index2 >= 0 else 0
            temp = t1 + t2 + add1
            result = str(temp % 2) + result
            add1 = temp // 2
            index1 -= 1
            index2 -= 1
        if add1 == 1:
            result = "1" + result

        return result

_ = Solution()
a = '11'
b = '1'
print(_.addBinary(a, b))