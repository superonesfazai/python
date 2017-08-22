# coding = utf-8

'''
@author = super_fazai
@File    : 查看线程数量.py
@Time    : 2017/8/9 16:28
@connect : superonesfazai@gmail.com
'''

import threading
from time import sleep,ctime

def sing():
    for i in range(3):
        print("正在唱歌...%d" % i)
        sleep(1)

def dance():
    for i in range(3):
        print("正在跳舞...%d" % i)
        sleep(1)

if __name__ == '__main__':
    print('---开始---:%s' % ctime())
    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)
    t1.start()
    t2.start()
    while True:
        length = len(threading.enumerate())         # threading.enumerate() -> Return a list of all Thread objects currently alive.
        print('当前运⾏的线程数为： %d' % length)
        if length <= 1:
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