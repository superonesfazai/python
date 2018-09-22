# coding = utf-8

'''
@author = super_fazai
@File    : 异步进程池.py
@connect : superonesfazai@gmail.com
'''

from multiprocessing import Pool
import time
import os

def test():
    print('---进程池中的进程---pid=%d, ppid=%d---' % (os.getpid(), os.getppid()))
    for i in range(3):
        print('---%d---' % i)
        time.sleep(1)
    return 'haha'

def test2(args):
    print("---callback func--pid=%d" % os.getpid())
    print("---callback func--args=%s" % args)

pool = Pool(3)
pool.apply_async(func=test, callback=test2)

time.sleep(5)

print("----主进程-pid=%d----"%os.getpid())

'''
测试结果:
---进程池中的进程---pid=6193, ppid=6191---
---0---
---1---
---2---
---callback func--pid=6191
---callback func--args=haha
----主进程-pid=6191----
'''