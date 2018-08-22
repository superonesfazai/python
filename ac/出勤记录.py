# coding:utf-8

"""
给定一个字符串来代表一个员工的出勤纪录，这个纪录仅包含以下三个字符：

'A' : Absent，缺勤
'L' : Late，迟到
'P' : Present，到场
如果一个员工的出勤纪录中不超过一个'A'(缺勤)并且不超过两个连续的'L'(迟到),那么这个员工会被奖赏。

你需要根据这个员工的出勤纪录判断他是否会被奖赏。

示例 1:
输入: "PPALLP"
输出: True

示例 2:
输入: "PPALLL"
输出: False
"""

class Solution(object):
    def checkRecord(self, s):
        """
        :type s: str
        :rtype: bool
        """
        return False if s.count('A') > 1 or 'LLL' in s else True

_ = Solution()
# s = "PPALLP"
# s = "PPALLL"
# s = 'PPPPPP'
s = 'LALL'
print(_.checkRecord(s))