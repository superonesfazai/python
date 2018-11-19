# coding = utf-8

'''
@author = super_fazai
@File    : 主线程会等待所有的子进程结束后才结束_test.py
@Time    : 2017/8/9 16:23
@connect : superonesfazai@gmail.com
'''

"""
threading: 其实是 线程模块仿真Java线程模型的一个子集
"""

# 主线程会等待所有的⼦线程结束后才结束

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
    sleep(5) # 屏蔽此⾏代码， 试试看， 程序是否会⽴⻢结束？
    print('---结束---:%s'%ctime())

'''
测试结果:
---开始---:Wed Aug  9 16:27:47 2017
正在唱歌...0
正在跳舞...0
正在唱歌...1
正在跳舞...1
正在唱歌...2
正在跳舞...2
---结束---:Wed Aug  9 16:27:52 2017
'''