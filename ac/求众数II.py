# coding:utf-8

"""
给定一个大小为 n 的数组，找出其中所有出现超过 ⌊ n/3 ⌋ 次的元素。

说明: 要求算法的时间复杂度为 O(n)，空间复杂度为 O(1)。

示例 1:
输入: [3,2,3]
输出: [3]

示例 2:
输入: [1,1,1,3,3,2,2,2]
输出: [1,2]
"""

class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        _ = set(nums)  # 避免大数导致时间超时
        res = []
        for i in _:
            if nums.count(i) > len(nums) / 3:
                if i not in res:
                    res.append(i)

        return res

_ = Solution()
nums = [3, 2, 3]
# nums = [2,2,1,1,1,2,2]
# nums = [1 for i in range(50001)]
print(_.majorityElement(nums))