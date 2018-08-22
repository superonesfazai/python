# coding:utf-8

"""
给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。

你可以假设数组中无重复元素。

eg1:
输入: [1,3,5,6], 5
输出: 2

eg2:
输入: [1,3,5,6], 2
输出: 1

eg:3
输入: [1,3,5,6], 7
输出: 4

eg:4
输入: [1,3,5,6], 0
输出: 0
"""

class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums = sorted(nums)

        for i in nums:
            if target == i:
                return nums.index(i)
            else:
                pass

        nums.append(target)
        a = sorted(nums)
        for i in a:
            if target == i:
                return a.index(target)

_ = Solution()
nums = [1,3,5,6]
target = 0
print(_.searchInsert(nums, target))