# coding = utf-8

'''
@author = super_fazai
@File    : multiprocess_test.py
@Time    : 2017/8/9 09:53
@connect : superonesfazai@gmail.com
'''

from multiprocessing import Process
import os

def run_proc(name):
    print('⼦进程运⾏中， name= %s ,pid=%d...' % (name, os.getpid()))

if __name__=='__main__':
    print('⽗进程 %d.' % os.getpid())
    p = Process(target=run_proc, args=('避免死锁',))
    print('⼦进程将要执⾏')
    p.start()
    p.join()
    print('⼦进程已结束')

'''
说明:
    1. 创建⼦进程时, 只需要传⼊⼀个执⾏函数和函数的参数, 
        创建⼀个Process实例, ⽤start()⽅法启动, 这样创建进程⽐fork()还要简单.
    2. join()⽅法可以等待⼦进程结束后再继续往下运⾏, 通常⽤于进程间的同步
'''

'''
测试结果:
⽗进程 5556.
⼦进程将要执⾏
⼦进程运⾏中， name= 避免死锁 ,pid=5557...
⼦进程已结束
'''