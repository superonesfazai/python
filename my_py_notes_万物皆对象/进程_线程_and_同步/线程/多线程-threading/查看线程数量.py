# coding = utf-8

'''
@author = super_fazai
@File    : 查看线程数量.py
@Time    : 2017/8/9 16:28
@connect : superonesfazai@gmail.com
'''

from threading import (
    Thread,
    enumerate,
    current_thread,
    active_count,)
from time import sleep, ctime

def sing():
    for i in range(3):
        print("正在唱歌...%d" % i)
        sleep(1)

    return 'sing over!'

def dance():
    for i in range(3):
        print("正在跳舞...%d" % i)
        sleep(1)

    return 'dance over!'

if __name__ == '__main__':
    print('---开始---:%s' % ctime())
    t1 = Thread(target=sing)
    t2 = Thread(target=dance)
    t1.start()
    t2.start()
    while True:
        # this method is the same to active_count().
        length = len(enumerate())         # threading.enumerate() -> Return a list of all Thread objects currently alive.
        print('当前运⾏的线程数为： %d' % length)
        if length <= 1:
            # print(t1.join())    # join()是阻塞调用
            print(current_thread())     # 即只剩下主线程_MainThread
            break
        sleep(0.5)

'''
测试结果:
---开始---:Wed Aug  9 16:31:41 2017
正在唱歌...0
正在跳舞...0
当前运⾏的线程数为： 3
当前运⾏的线程数为： 3
正在唱歌...1
正在跳舞...1
当前运⾏的线程数为： 3
当前运⾏的线程数为： 3
正在唱歌...2
正在跳舞...2
当前运⾏的线程数为： 3
当前运⾏的线程数为： 3
当前运⾏的线程数为： 1
'''