# coding = utf-8

'''
@author = super_fazai
@File    : operator_比较运算符.py
@Time    : 2017/8/16 23:06
@connect : superonesfazai@gmail.com
'''

"""
The functions are equivalent to the expression syntax using <, <=, ==, >=, and >.
"""

from operator import *

a = 1
b = 5.0

print('a =', a)
print('b =', b)
for func in (lt, le, eq, ne, ge, gt):
    print('{}(a, b): {}'.format(func.__name__, func(a, b)))

