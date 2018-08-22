# coding:utf-8

"""
给定两个字符串 s 和 t，它们只包含小写字母。

字符串 t 由字符串 s 随机重排，然后在随机位置添加一个字母。

请找出在 t 中被添加的字母。

eg:
输入：
s = "abcd"
t = "abcde"

输出：
e

解释：
'e' 是那个被添加的字母。
"""

class Solution(object):
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        s = sorted(s)
        t = sorted(t)
        # print(s)
        # print(t)

        # 切记: 不要在遍历同一集合时进行删除操作
        for i in s:
            if i in t:
                t.remove(i)

        return t[0]

_ = Solution()
# s = 'abccd'
# t = 'acbcde'
s = 'a'
t = 'aa'
print(_.findTheDifference(s, t))