# coding = utf-8

'''
@author = super_fazai
@File    : multiprocessing_Process_demo1.py
@Time    : 2017/8/9 10:04
@connect : superonesfazai@gmail.com
'''

from multiprocessing import Process
import os
from time import sleep

def run_proc(name, age, **kwargs):
    for i in range(10):
        print('⼦进程运⾏中， name= %s,age=%d ,pid=%d...' % (name, age,os.getpid()))
        print(kwargs)
        sleep(0.5)

if __name__=='__main__':
    print('⽗进程 %d.' % os.getpid())
    p = Process(target=run_proc, args=('避免死锁.md',18), kwargs={"m":20})
    print('⼦进程将要执⾏')
    p.start()
    sleep(1)
    p.terminate()
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
⽗进程 5622.
⼦进程将要执⾏
⼦进程运⾏中， name= 避免死锁.md,age=18 ,pid=5623...
{'m': 20}
⼦进程运⾏中， name= 避免死锁.md,age=18 ,pid=5623...
{'m': 20}
⼦进程已结束
'''