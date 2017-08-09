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
    p = Process(target=run_proc, args=('避免死锁',18), kwargs={"m":20})
    print('⼦进程将要执⾏')
    p.start()
    sleep(1)
    p.terminate()
    p.join()
    print('⼦进程已结束')

'''
测试结果:
⽗进程 5622.
⼦进程将要执⾏
⼦进程运⾏中， name= 避免死锁,age=18 ,pid=5623...
{'m': 20}
⼦进程运⾏中， name= 避免死锁,age=18 ,pid=5623...
{'m': 20}
⼦进程已结束
'''