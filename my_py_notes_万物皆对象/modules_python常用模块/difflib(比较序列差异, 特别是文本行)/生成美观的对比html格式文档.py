# coding:utf-8

'''
@author = super_fazai
@File    : 生成美观的对比html格式文档.py
@Time    : 2018/5/18 14:48
@connect : superonesfazai@gmail.com
'''

import difflib

text1 = r'''
import cmath

print(cmath.exp(2))     # return the exponential value e**x

print(cmath.sqrt(4))    # 开方

print(cmath.asin(0.5))

print('%.20f' % cmath.pi)
'''

text2 = r'''
import cmath
import sys

print(cmath.exp(2))     # return the exponential value e**x

print(cmath.sqrt(4))    # 开方

print(cmath.asin(0.6))

print('%.200f' % cmath.pi)
'''

text1 = text1.splitlines()
text2 = text2.splitlines()

# d = difflib.Differ()
# diff = d.compare(text1, text2)
# print('\n'.join(list(diff)))

# 替换成

d = difflib.HtmlDiff()
d_html_code = d.make_file(text1, text2)

with open('diff_html.html', 'wb') as f:
    f.write(d_html_code.encode('utf-8'))