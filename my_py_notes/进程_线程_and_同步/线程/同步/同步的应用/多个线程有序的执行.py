# coding = utf-8

'''
@author = super_fazai
@File    : 多个线程有序的执行.py
@Time    : 2017/8/9 17:42
@connect : superonesfazai@gmail.com
'''

# 可以使⽤互斥锁完成多个任务， 有序的进程⼯作， 这就是线程的同步

from threading import Thread,Lock
from time import sleep

class Task1(Thread):
    def run(self):
        while True:
            if lock1.acquire():
                print("------Task 1 -----")
                sleep(0.5)
                lock2.release()

class Task2(Thread):
    def run(self):
        while True:
            if lock2.acquire():
                print("------Task 2 -----")
                sleep(0.5)
                lock3.release()

class Task3(Thread):
    def run(self):
        while True:
            if lock3.acquire():
                print("------Task 3 -----")
                sleep(0.5)
                lock1.release()

#使⽤Lock创建出的锁默认没有“锁上”
lock1 = Lock()
#创建另外⼀把锁， 并且“锁上”
lock2 = Lock()
lock2.acquire()
#创建另外⼀把锁， 并且“锁上”
lock3 = Lock()
lock3.acquire()
t1 = Task1()
t2 = Task2()
t3 = Task3()
t1.start()
t2.start()
t3.start()

'''
测试结果:
------Task 1 -----
------Task 2 -----
------Task 3 -----
------Task 1 -----
------Task 2 -----
------Task 3 -----
------Task 1 -----
------Task 2 -----
------Task 3 -----
------Task 1 -----
------Task 2 -----
------Task 3 -----
------Task 1 -----
------Task 2 -----
------Task 3 -----
------Task 1 -----
------Task 2 -----
------Task 3 -----
...
'''