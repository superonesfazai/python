# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2017/8/16 18:53
@connect : superonesfazai@gmail.com
'''

from time import sleep
import ray

# 普通python code
# 连续的执行f函数
print('普通')
def f():
    print('sleep 1s ...')
    sleep(1)
    return 1

_ = [f() for i in range(4)]

# 通过ray实现分布式
# 并发执行f函数
print('ray')
@ray.remote
def f():
    print('sleep 1s ...')
    sleep(1)
    return 1

ray.init()
_ = ray.get([f.remote() for i in range(4)])