# coding = utf-8

'''
@author = super_fazai
@File    : re_findall_test.py
@Time    : 2017/8/18 16:27
@connect : superonesfazai@gmail.com
'''

import re

# 语法: findall(string[, pos[, endpos]])

# findall()返回的是list类型
res = re.findall(r"\d+", "python = 9999, c = 7890, c++ = 12345")
print(res)