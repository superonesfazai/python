# coding:utf-8

"""
给定两个数组，编写一个函数来计算它们的交集。

eg1:
输入: nums1 = [1,2,2,1], nums2 = [2,2]
输出: [2]

eg2:
输入: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出: [9,4]

说明:

输出结果中的每个元素一定是唯一的。
我们可以不考虑输出结果的顺序。
"""

class Solution(object):
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        nums1 = sorted(nums1)
        nums2 = sorted(nums2)

        _, _2 =  (nums1, nums2) if len(nums1) > len(nums2) else (nums2, nums1)
        # print(_)
        # print(_2)

        result = []
        for i in _:
            if i in _2:
                if i not in result:
                    result.append(i)

        return result

_ = Solution()
# nums1 = [1,2,2,1]
# nums2 = [2,2]
nums1 = [4,9,5]
nums2 = [9,4,9,8,4]
# nums1 = [1,1]
# nums2 = [1,2]
print(_.intersection(nums1, nums2))
