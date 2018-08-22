# coding:utf-8

"""
给定一个大小为 n 的数组，找到其中的众数。众数是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在众数。

示例 1:
输入: [3,2,3]
输出: 3

示例 2:
输入: [2,2,1,1,1,2,2]
输出: 2
"""

class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        _ = set(nums)   # 避免大数导致时间超时
        for i in _:
            if nums.count(i) > len(nums)/2:
                return i

_ = Solution()
# nums = [3, 2, 3]
# nums = [2,2,1,1,1,2,2]
nums = [1 for i in range(50001)]
print(_.majorityElement(nums))