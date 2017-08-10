#!/usr/bin/python3.5
#coding:utf-8

from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)        # put中的block默认为Ture, 为阻塞式
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:         # 如果判断条件改为 while not q.empty(): 则由于睡的时间不同, 可能导致读数据提停止
        value = q.get()     # get中的block默认为True， 为阻塞式
        print('Get %s from queue.' % value)

if __name__=='__main__':
    q = Queue()         # 父进程创建Queue，并传给各个子进程
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))

    pw.start()          # 启动子进程pw，写入
    pr.start()          # 启动子进程pr，读取

    pw.join()           # 等待pw结束
    pr.terminate()      # pr进程里是死循环，无法等待其结束，只能强行终止

    print('所有数据都以写入并且读完')


'''
测试结果:
Process to write: 6249
Put A to queue...
Process to read: 6250
Get A from queue.
Put B to queue...
Get B from queue.
Put C to queue...
Get C from queue.
所有数据都以写入并且读完
'''