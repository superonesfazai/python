# coding = utf-8

'''
@author = super_fazai
@File    : re_split_test.py
@Time    : 2017/8/18 16:34
@connect : superonesfazai@gmail.com
'''

"""
split 根据匹配进行切割字符串, 并返回一个列表
"""

import re

res = re.split(r':| ', 'info:xiaoZhang 33 shandong')
print(res)

'''
测试结果:
['info', 'xiaoZhang', '33', 'shandong']
'''