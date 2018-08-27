# coding:utf-8

"""
给定两个有序整数数组 nums1 和 nums2，将 nums2 合并到 nums1 中，使得 num1 成为一个有序数组。

说明:

初始化 nums1 和 nums2 的元素数量分别为 m 和 n。
你可以假设 nums1 有足够的空间（空间大小大于或等于 m + n）来保存 nums2 中的元素。

示例:
输入:
nums1 = [1,2,3,0,0,0], m = 3
nums2 = [2,5,6],       n = 3

输出: [1,2,2,3,5,6]
"""

class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: void Do not return anything, modify nums1 in-place instead.
        """
        nums1 = nums1[0:m]
        nums2 = nums2[0:n]

        for i in nums2:
            nums1.append(i)

        length = len(nums1)
        for i in range(length - 1, -1, -1):
            for j in range(i):
                if nums1[j] > nums1[j + 1]:
                    nums1[j], nums1[j + 1] = nums1[j + 1], nums1[j]

        nums1 = sorted(nums1)
        # print(nums1)


_ = Solution()
nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3
# nums1 = [-1,0,0,3,3,3,0,0,0]
# m = 6
# nums2 = [1,2,2]
# n = 3
print(_.merge(nums1, m, nums2, n))