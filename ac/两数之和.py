# coding:utf-8

"""
给定一个整数数组和一个目标值，找出数组中和为目标值的两个数。

你可以假设每个输入只对应一种答案，且同样的元素不能被重复利用。

eg:
给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]

题意: 两数不等, 返回值索引正序
"""

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for index, item in enumerate(nums):
            o = target - item
            try:
                index_2 = nums.index(o)
            except ValueError:
                continue

            if index_2 == index:
                continue

            return sorted([index, index_2])

nums = [3,2,4]
# nums = [3, 3]
target = 6

_ = Solution()
print(_.twoSum(nums, target))