# coding = utf-8

'''
@author = super_fazai
@File    : re_sub_test.py
@Time    : 2017/8/18 16:29
@connect : superonesfazai@gmail.com
'''

# sub 将匹配到的数据进行替换

import re

res = re.sub(r"\d+", '998', "python = 997")
print(res)

res = re.sub(
    r'(\d{4})-(\d{2})-(\d{2})',
    r'\2/\3/\1',
    '2017-01-01')
print(res)

res = re.sub(   # (?=xx)从左向右匹配, 符合内容的字符串后面加空格
    '(?=\d{3})',
    ' ',
    'abc12345def'
)
print(res)

res = re.sub(   # (?!=xx)和上面效果正好相反, 也是后面加空格
    '(?!\d{3})',
    ' ',
    'abc12345def'
)
print(res)

res = re.sub(   # (?<=xx)从右向左匹配, 符合内容的字符串后面加空格
    '(?<=\d{3})',
    ' ',
    'abc12345def'
)
print(res)

res = re.sub(   # (?<!xx)和上面效果正好相反, 也是后面加空格
    '(?<!\d{3})',
    ' ',
    'abc12345def'
)
print(res)

'''
测试结果:
python = 998
01/01/2017
abc 1 2 345def
 a b c123 4 5 d e f 
abc123 4 5 def
 a b c 1 2 345d e f
'''