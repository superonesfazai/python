# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午12:15
# @File    : 生成器_test.py

# 生成器(generator)
# 从语法上讲: 生成器是一个带yield语句的函数
# 生成器是一种特殊的迭代器
# 生成器的运作方式:当到达一个真正返回或者函数接受没有更多的值返回(当调用next()), 一个StopIteration()异常会抛出

# 下面是一个简单的生成器
def simple_gen():
    yield 1
    yield '2 --> punch!'

mg_g = simple_gen()
print(mg_g.__next__())
print(mg_g.__next__())
try:
    print(mg_g.__next__())
except StopIteration as e:
    print(e, 'this is StopIteration')
    print('')

# for循环的本质
# 1. 先调用可迭代对象的__iter__方法得到一个可迭代对象
# 2. 由于python的for循环中有__next__(),和对StopIteration的处理,所以使用一个for循环而不是手动迭代穿过一个生成器,总是简洁漂亮很多
# eg:
for each_item in simple_gen():
    print(each_item)

print('')

# 接下来我创建一个带序列并从那个序列返回一个随机元素的随机迭代器
from random import randint
def rand_gen(a_list):
    while len(a_list) > 0:
        yield a_list.pop(randint(0, len(a_list)-1))

for item in rand_gen(['a', 'b', 'c']):
    print(item)

print('')

# 加强的生成器的特性
# 除了__next__()来获得下一个生成的值
# 用户可以将值回送给生成器[send()]
# 在生成器中抛出异常
# 以及要求生成器退出[close()]

# 由于双向的动作涉及叫做send()的代码来向生成器发送值(以及生成器返回的值发送回来),所以现在yield语句必须是一个表达式
def counter(start_at = 0):
    count = start_at
    while True:
        val = (yield count)
        if val is not None:
            count = val
        else:
            count += 1

count = counter(5)
print(count.__next__())
print(count.__next__())
print(count.send(9))
print(count.__next__())
count.close()
try:
    count.__next__()
except StopIteration as e:
    print(e, 'this is a StopIteration!')

