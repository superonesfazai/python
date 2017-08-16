# coding = utf-8

'''
@author = super_fazai
@File    : operator_boolean.py
@Time    : 2017/8/16 23:04
@connect : superonesfazai@gmail.com
'''

from operator import *

a = -1
b = 5

print('a =', a)
print('b =', b)
print()

print('not_(a)     :', not_(a))
print('truth(a)    :', truth(a))        # truth()应用在测试if语句中的表达式或将表达式转换为a 时使用的逻辑相同的逻辑bool
print('is_(a, b)   :', is_(a, b))       # is_()实现is关键字使用的相同检查
print('is_not(a, b):', is_not(a, b))    # is_not()进行相同的测试并返回相反的答案