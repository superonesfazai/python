# coding:utf-8

"""
给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

示例:
输入："23"
输出：["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
说明:
尽管上面的答案是按字典序排列的，但是你可以任意选择答案输出的顺序。
"""

class Solution(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        p = {
            '2': ['a', 'b', 'c'],
            '3': ['d', 'e', 'f'],
            '4': ['g', 'h', 'i'],
            '5': ['j', 'k', 'l'],
            '6': ['m', 'n', 'o'],
            '7': ['p', 'q', 'r', 's'],
            '8': ['t', 'u', 'v'],
            '9': ['w', 'x', 'y', 'z'],
        }

        digits = [i for i in digits]
        _ = []
        for key, value in p.items():
            for i in digits:
                if key == i:
                    _.append(value)

        print(_)
        res = []
        if len(_) == 0:
            return []
        elif len(_) == 1:
            return _[0]
        else:
            for index, i in enumerate(_[:-1]):
                for index2, j in enumerate(i):
                    for index3, l in enumerate(_[index+1]):
                        tmp = j+l
                        res.append(tmp)

        return list(set(res))

_ = Solution()
a = '22'
print(_.letterCombinations(a))