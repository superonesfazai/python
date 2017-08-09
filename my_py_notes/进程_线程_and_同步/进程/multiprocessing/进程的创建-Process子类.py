# coding = utf-8

'''
@author = super_fazai
@File    : 进程的创建-Process子类.py
@Time    : 2017/8/9 10:31
@connect : superonesfazai@gmail.com
'''

from multiprocessing import Process
import os
import time

# 继承Process类
class Process_Class(Process):
    def __init__(self, interval):
        Process.__init__(self)
        self.interval = interval
    # 重写Process类的run()方法
    def run(self):
        print("⼦进程(%s) 开始执⾏， ⽗进程为（ %s） " % (os.getpid(), os.getppid()))
        t_start = time.time()
        time.sleep(self.interval)
        t_stop = time.time()
        print("(%s)执⾏结束， 耗时%0.2f秒" % (os.getpid(), t_stop - t_start))

if __name__ == "__main__":
    t_start = time.time()
    print("当前程序进程(%s)" % os.getpid())
    p1 = Process_Class(2)       # 对⼀个不包含target属性的Process类执⾏start()⽅法, 就会运⾏这个类中的run()⽅法, 所以这⾥会执⾏p1.run()
    p1.start()
    p1.join()
    t_stop = time.time()
    print("(%s)执⾏结束， 耗时%0.2f" % (os.getpid(), t_stop - t_start))

'''
测试结果:
当前程序进程(5820)
⼦进程(5821) 开始执⾏， ⽗进程为（ 5820） 
(5821)执⾏结束， 耗时2.00秒
(5820)执⾏结束， 耗时2.01
'''