# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import re

a = [1.6, 23, 1.8, 34]

price = [a[index] for index in range(0, len(a)) if index % 2 == 0 or index == 0]
rest = [a[index] for index in range(0, len(a)) if index % 2 != 0 and index != 0]
print(price)
print(rest)

print('-' * 100)

b = ['\n                                        ', '\n                                    ', '\n                                        ', '\n                                    ']
c = []
for item in b:
    tmp = re.compile(r'\n').sub('', item)
    tmp = re.compile(r' ').sub('', tmp)

    if tmp == '':
        pass
    else:
        c.append(tmp)
print(b)
print(c)

print('-' * 100)

d = 'https://cbu01.alicdn.com/img/ibank/2017/655/128/4704821556_608602289.60x60.jpg'

d = re.compile(r'\.60x60\.').sub('.400x400.', d)
print(d)