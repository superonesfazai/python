# coding = utf-8

'''
@author = super_fazai
@File    : re_finditer_test.py
@Time    : 2017/8/29 10:34
@connect : superonesfazai@gmail.com
'''

"""
finditer 方法的行为跟 findall 的行为类似，也是搜索整个字符串，获得所有匹配的结果。
但它返回一个顺序访问每一个匹配结果（Match 对象）的迭代器
"""

import re
pattern = re.compile(r'\d+')

result_iter1 = pattern.finditer('hello 123456 789')
result_iter2 = pattern.finditer('one1two2three3four4', 0, 10)

print(type(result_iter1))
print(type(result_iter2))

print('result1...')
for m1 in result_iter1:   # m1 是 Match 对象
    print('matching string: {}, position: {}'.format(m1.group(), m1.span()))

print('result2...')
for m2 in result_iter2:
    print('matching string: {}, position: {}'.format(m2.group(), m2.span()))

'''
测试结果:
<class 'callable_iterator'>
<class 'callable_iterator'>
result1...
matching string: 123456, position: (6, 12)
matching string: 789, position: (13, 16)
result2...
matching string: 1, position: (3, 4)
matching string: 2, position: (7, 8)
'''