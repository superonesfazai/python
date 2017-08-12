# coding = utf-8

'''
@author = super_fazai
@File    : 非阻塞方式使用互斥锁.py
@Time    : 2017/8/12 09:09
@connect : superonesfazai@gmail.com
'''

from threading import Thread, Lock
import time

g_num = 0
def test1():
    global g_num
    for i in range(1000000):
        while True:
            # 1. True表示堵塞 即如果这个锁在上锁之前已经被上锁了, 那么这个线程会在这⾥⼀直等待到解锁为⽌
            # 2. False表示⾮堵塞, 即不管本次调⽤能够成功上锁, 都不会卡在这, ⽽是继续执⾏下⾯的代码
            mutexFlag = mutex.acquire(blocking=False)     # 默认blocking为Ture, 即阻塞状态, 改为False为非阻塞状态
            if mutexFlag:   # 非阻塞有时会返回Ture, 有时会返回False；而阻塞状态返回值永远为True，会卡在上面那句话
                g_num += 1
                mutex.release()     # 释放锁, 表示将锁设置为未上锁状态
                break
            else:
                # time.sleep(0.01)
                pass
    print("---test1---g_num=%d"%g_num)

def test2():
    global g_num
    for i in range(1000000):
        while True:
            mutexFlag = mutex.acquire(blocking=False) # True表示堵塞
            if mutexFlag:
                g_num += 1
                mutex.release()
                break
            else:
                # time.sleep(0.01)
                pass
    print("---test2---g_num=%d"%g_num)

# 创建⼀个互斥锁
# 这个锁默认是未上锁的状态
mutex = Lock()
p1 = Thread(target=test1)
p1.start()
p2 = Thread(target=test2)
p2.start()
print("---g_num=%d---"%g_num)
