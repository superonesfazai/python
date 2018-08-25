# coding:utf-8

"""
编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 ""。

示例 1:
输入: ["flower","flow","flight"]
输出: "fl"

示例 2:
输入: ["dog","racecar","car"]
输出: ""
解释: 输入不存在公共前缀。

说明:
所有输入只包含小写字母 a-z
"""

class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        import re

        res = ''
        s = ''
        try:
            strs[0]
        except IndexError:
            return ''
        for l in strs[0]:
            s += l
            # print(s)
            for i in strs:
                if re.compile('^'+s).findall(i) != []:
                    pass
                else:
                    break
            else:
                res = s

        return res

_ = Solution()
a = ["flower","flow","flight"]
# a = ["dog","racecar","car"]
print('->', _.longestCommonPrefix(a))
