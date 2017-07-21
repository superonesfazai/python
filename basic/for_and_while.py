#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

#python 的循环有两种
#一种是for...in循环，依次把list或tuple中的每个元素迭代出来
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
print('')

sum = 0
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    sum = sum + x
print(sum)
print('')

#遍历数字序列
for x in range(3):
	print(x)
print('')

#使用range指定区间的值
for i in range(6,9):
	print(i)
print('')

#使range以指定数字开始并指定不同的增量(甚至可以是负数，有时这也叫做'步长')
for i in range(0, 10, 3) :
	print(i)
print('')

#可以结合range()和len()函数以遍历一个序列的索引
a = ['Google', 'Baidu', 'Runoob', 'Taobao', 'QQ']
for i in range(len(a)):
	print(i, a[i])
print('')

#生成一个整数序列
print(list(range(5)))
print('')

#第二种循环是while循环
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)

#break语句可以提前退出循环

#通过continue语句，跳过当前的这次循环，直接开始下一次循环

import os
for k, v in os.environ.items():
    print('%s=%s' % (k, v))