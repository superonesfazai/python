# coding = utf-8

'''
@author = super_fazai
@File    : 多进程修改全局变量测试.py
@Time    : 2017/8/9 09:38
@connect : superonesfazai@gmail.com
'''

import os
import time

num = 0
# 注意， fork函数, 只在Unix/Linux/Mac上运⾏， windows不可以
pid = os.fork()

if pid == 0:
    num+=1
    print('哈哈1---num=%d'%num)
else:
    time.sleep(1)
    num+=1
    print('哈哈2---num=%d'%num)

'''
测试结果:
哈哈1---num=1
哈哈2---num=1
'''

'''
总结：
    多进程中, 每个进程中所有数据(包括全局变量) 都各有拥有⼀份， 互
    不影响 (读时共享， 写时复制)
'''