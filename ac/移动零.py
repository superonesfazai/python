# coding:utf-8

"""
给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

eg:
输入: [0,1,0,3,12]
输出: [1,3,12,0,0]

说明:

必须在原数组上操作，不能拷贝额外的数组。
尽量减少操作次数。
"""

class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        zero_num = 0
        for index, item in enumerate(nums):
            if item == 0:
                nums.pop(index)
                zero_num += 1
            else:
                pass

        nums += [0 for i in range(zero_num)]

        return nums

_ = Solution()
a = [0,1,0,3,12]
# nums = [0,0]
print(_.moveZeroes(a))