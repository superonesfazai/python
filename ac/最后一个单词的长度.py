# coding:utf-8

"""
给定一个仅包含大小写字母和空格 ' ' 的字符串，返回其最后一个单词的长度。

如果不存在最后一个单词，请返回 0 。

说明：一个单词是指由字母组成，但不包含任何空格的字符串。

eg:
输入: "Hello World"
输出: 5
"""

class Solution(object):
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """
        import re

        while True: # 先处理替换掉多余空格
            re_c = re.compile('  ')
            if re_c.findall(s) != []:
                s = re_c.sub(' ', s)
            else:
                break

        # print(s)
        s_list = s.split(' ')
        for index, i in enumerate(s_list):  # 去除''
            if i == '':
                s_list.pop(index)

        result = len(s_list[-1]) if s_list != [] else 0

        return result

_ = Solution()
# s = 'Hello World'
s = 'a  '
print(_.lengthOfLastWord(s))