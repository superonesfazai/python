# coding:utf-8

"""
给定一个整数数组，判断是否存在重复元素。

如果任何值在数组中出现至少两次，函数返回 true。如果数组中每个元素都不相同，则返回 false。

eg1:
输入: [1,2,3,1]
输出: true

eg2:
输入: [1,2,3,4]
输出: false

eg3:
输入: [1,1,1,3,3,4,3,2,4,2]
输出: true
"""

class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        result = False
        for item in nums:
            if nums.count(item) > 1:
                result = True
                break

        return result

_ = Solution()
# a = [1,2,3,1]
a = [1,2,3,4]
# a = [1,1,1,3,3,4,3,2,4,2]
print(_.containsDuplicate(a))