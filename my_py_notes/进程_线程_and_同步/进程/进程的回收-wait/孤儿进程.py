# coding = utf-8

'''
@author = super_fazai
@File    : 孤儿进程.py
@Time    : 2017/8/9 09:17
@connect : superonesfazai@gmail.com
'''

# 子进程还未运行完成, 父进程就结束运行退出, 留下的子进程就叫做孤儿进程
# 父进程死掉后, 孤儿进程会被别的进程收养, 通常是init进程(pid=1)
# 因为孤儿进程最终会被继父回收, 所以没有什么危害

import os
import time

pid = os.fork()

if pid == 0:
    for i in range(100):
        print('子进程%d工作中...父进程pid为%d' % (os.getpid(), os.getppid()))
        time.sleep(3)
        # print('---')
else:
    print('父进程%d为父先走一步, 儿要保重' % (os.getpid(),))
    os.system('kill -9 %d' % (os.getpid(),))    # os.system()没有返回值
