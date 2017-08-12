# coding = utf-8

'''
@author = super_fazai
@File    : 死锁_demo.py
@Time    : 2017/8/9 18:10
@connect : superonesfazai@gmail.com
'''

'''
在线程间共享多个资源的时候, 如果两个线程分别占有⼀部分资源并且同时等待对⽅的资源, 就会造成死锁.
尽管死锁很少发⽣. 但⼀旦发⽣就会造成应⽤的停⽌响应

解决方案:
    1. 设置成非阻塞的
    2. 或者设置超时等待时间, 如果一个锁对一个资源上不了锁, 就先让之前的锁先让步解锁
'''

import threading
import time

class MyThread1(threading.Thread):
    def run(self):
        if mutexA.acquire():            # 对mutexA这个锁进行了上锁
            print(self.name+'----do1---up----')
            time.sleep(1)
            if mutexB.acquire():        # 互相等待对方释放锁, 然后上锁, 但事与愿违
                print(self.name+'----do1---down----')
                mutexB.release()
            mutexA.release()

class MyThread2(threading.Thread):
    def run(self):
        if mutexB.acquire():            # 对mutexB这个锁进行上锁
            print(self.name+'----do2---up----')
            time.sleep(1)
            if mutexA.acquire():        # 互相等待对方释放锁, 然后上锁, 但事与愿违
                print(self.name+'----do2---down----')
                mutexA.release()
            mutexB.release()

mutexA = threading.Lock()
mutexB = threading.Lock()

if __name__ == '__main__':
    t1 = MyThread1()
    t2 = MyThread2()
    t1.start()
    t2.start()

# 此时已经进⼊到了死锁状态， 可以使⽤ctrl-c退出