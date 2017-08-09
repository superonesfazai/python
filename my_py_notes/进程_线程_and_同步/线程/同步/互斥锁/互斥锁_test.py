# coding = utf-8

'''
@author = super_fazai
@File    : 互斥锁_test.py
@Time    : 2017/8/9 17:22
@connect : superonesfazai@gmail.com
'''

from threading import Thread, Lock
import time

g_num = 0
def test1():
    global g_num
    for i in range(1000000):
        # True表示堵塞 即如果这个锁在上锁之前已经被上锁了, 那么这个线程会在这⾥⼀直等待到解锁为⽌
        # False表示⾮堵塞, 即不管本次调⽤能够成功上锁, 都不会卡在这, ⽽是继续执⾏下⾯的代码
        mutexFlag = mutex.acquire(True)
        if mutexFlag:
            g_num += 1
            mutex.release()
    print("---test1---g_num=%d"%g_num)

def test2():
    global g_num
    for i in range(1000000):
        mutexFlag = mutex.acquire(True) # True表示堵塞
        if mutexFlag:
            g_num += 1
            mutex.release()
    print("---test2---g_num=%d"%g_num)

# 创建⼀个互斥锁
# 这个所默认是未上锁的状态
mutex = Lock()
p1 = Thread(target=test1)
p1.start()
p2 = Thread(target=test2)
p2.start()
print("---g_num=%d---"%g_num)

'''
上锁解锁过程
    1. 当⼀个线程调⽤锁的acquire()⽅法获得锁时, 锁就进⼊“locked”状态.
    2. 每次只有⼀个线程可以获得锁. 如果此时另⼀个线程试图获得这个锁, 该线
        程就会变为“blocked”状态, 称为“阻塞”, 直到拥有锁的线程调⽤锁的
    3. release()⽅法释放锁之后， 锁进⼊“unlocked”状态。
    4. 线程调度程序从处于同步阻塞状态的线程中选择⼀个来获得锁， 并使得该线
    程进⼊运⾏（ running） 状态
'''

'''
测试过程:
---g_num=27934---
---test1---g_num=1938997
---test2---g_num=2000000
'''