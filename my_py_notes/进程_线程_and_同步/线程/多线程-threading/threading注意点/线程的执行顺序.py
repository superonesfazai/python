# coding = utf-8

'''
@author = super_fazai
@File    : 线程的执行顺序.py
@Time    : 2017/8/9 16:46
@connect : superonesfazai@gmail.com
'''

'''
多线程程序的执⾏顺序是不确定的. 
当执⾏到sleep语句时, 线程将被阻塞(Blocked), 到sleep结束后 
线程进⼊就绪(Runnable)状态, 等待调度. ⽽线程调度将⾃⾏选择⼀个线程执⾏
'''

import threading
import time

class MyThread(threading.Thread):
    def run(self):
        for i in range(3):
            time.sleep(1)
            msg = 'I\'m' + self.name + ' @ ' + str(i)
            print(msg)

def test():
    for i in range(5):
        t = MyThread()
        t.start()

if __name__ == '__main__':
    test()

'''
测试结果:
I'mThread-1 @ 0
I'mThread-3 @ 0
I'mThread-5 @ 0
I'mThread-2 @ 0
I'mThread-4 @ 0
I'mThread-3 @ 1
I'mThread-1 @ 1
I'mThread-5 @ 1
I'mThread-2 @ 1
I'mThread-4 @ 1
I'mThread-3 @ 2
I'mThread-4 @ 2
I'mThread-1 @ 2
I'mThread-2 @ 2
I'mThread-5 @ 2
'''

'''
上⾯的代码中只能保证每个线程都运⾏完整个run函数,
但是线程的启动顺序、run函数中每次循环的执⾏顺序都不能确定
'''