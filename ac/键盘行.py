# coding:utf-8

"""
给定一个单词列表，只返回可以使用在键盘同一行的字母打印出来的单词。键盘如下图所示。

示例1:
输入: ["Hello", "Alaska", "Dad", "Peace"]
输出: ["Alaska", "Dad"]
注意:

你可以重复使用键盘上同一字符。
你可以假设输入的字符串将只包含字母。
"""


class Solution(object):
    def findWords(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """
        line1 = 'qwertyuiop'
        line2 = 'asdfghjkl'
        line3 = 'zxcvbnm'

        res = []
        for i in words:
            tab_list = []
            for j in i:
                # print(j)
                if j in line1:
                    tab_list.append(1)
                elif j in line2:
                    tab_list.append(2)
                elif j in line3:
                    tab_list.append(3)
                else:
                    pass

            if len(set(tab_list)) == 1:
                res.append(i)

        return res

_ = Solution()
words = ["Hello", "Alaska", "Dad", "Peace", 'aqz']
print(_.findWords(words))