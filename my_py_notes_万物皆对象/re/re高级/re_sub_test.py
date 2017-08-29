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

# 语法: sub(repl, string[, count]) 先compile(),再使用sub

'''
其中，repl 可以是字符串也可以是一个函数：
    如果 repl 是字符串，则会使用 repl 去替换字符串每一个匹配的子串，并返回替换后的字符串，另外，repl 还可以使用 id 的形式来引用分组，但不能使用编号 0；
    
    如果 repl 是函数，这个方法应当只接受一个参数（Match 对象），并返回一个字符串用于替换（返回的字符串中不能再引用分组）。
    
    count 用于指定最多替换次数，不指定时全部替换
'''

print('分割线'.center(40, '-'))

import re
p = re.compile(r'(\w+) (\w+)') # \w = [A-Za-z0-9]
s = 'hello 123, hello 456'

print(p.sub(r'hello world', s))  # 使用 'hello world' 替换 'hello 123' 和 'hello 456'
print(p.sub(r'\2 \1', s))        # 引用分组

def func(m):
    return 'hi' + ' ' + m.group(2)

print(p.sub(func, s))
print(p.sub(func, s, 1))         # 最多替换一次

'''
测试结果:
python = 998
01/01/2017
abc 1 2 345def
 a b c123 4 5 d e f 
abc123 4 5 def
 a b c 1 2 345d e f 
------------------分割线-------------------
hello world, hello world
123 hello, 456 hello
hi 123, hi 456
hi 123, hello 456
'''