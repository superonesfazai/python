# coding = utf-8

'''
@author = super_fazai
@File    : 列表推导很快_但发电机更快吗?.py
@Time    : 2017/8/18 21:05
@connect : superonesfazai@gmail.com
'''

"""
“列表推理速度很快，但发电机更快！” - 不，不是（或者显着地看下面的基准）。那么什么原因更喜欢一个呢？

    * 如果您想使用多种列表方法，请使用列表
    * 当您处理巨大的集合以避免内存问题时使用生成器
"""

'''
记住:
在某些情况下（即，当我们处理大量计算时）我们喜欢使用列表推导式的主要原因是它仅在需要时计算下一个值，也称为“惰性”评估。但是，生成器的第一个子句在创建时已经被检查
'''

import timeit

def plainlist(n=100000):
    my_list = []
    for i in range(n):
        if i % 5 == 0:
            my_list.append(i)
    return my_list

def listcompr(n=100000):
    my_list = [i for i in range(n) if i % 5 == 0]
    return my_list

def generator(n=100000):
    my_gen = (i for i in range(n) if i % 5 == 0)
    return my_gen

def generator_yield(n=100000):
    for i in range(n):
        if i % 5 == 0:
            yield i

# 为了公平的列表，让我们耗尽发电机：

def test_plainlist(plain_list):
    for i in plain_list():
        pass

def test_listcompr(listcompr):
    for i in listcompr():
        pass

def test_generator(generator):
    for i in generator():
        pass

def test_generator_yield(generator_yield):
    for i in generator_yield():
        pass

print('plain_list:     ', end = '')
%timeit test_plainlist(plainlist)
print('\nlistcompr:     ', end = '')
%timeit test_listcompr(listcompr)
print('\ngenerator:     ', end = '')
%timeit test_generator(generator)
print('\ngenerator_yield:     ', end = '')
%timeit test_generator_yield(generator_yield)

"""
测试结果:
plain_list:     10 loops, best of 3: 22.4 ms per loop

listcompr:     10 loops, best of 3: 20.8 ms per loop

generator:     10 loops, best of 3: 22 ms per loop

generator_yield:     10 loops, best of 3: 21.9 ms per loop
"""