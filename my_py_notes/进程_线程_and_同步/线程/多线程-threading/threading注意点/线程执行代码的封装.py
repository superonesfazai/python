# coding = utf-8

'''
@author = super_fazai
@File    : 线程执行代码的封装.py
@Time    : 2017/8/9 16:34
@connect : superonesfazai@gmail.com
'''

'''
通过使⽤threading模块能完成多任务的程序开发
为了让每个线程的封装性更完美, 所以使⽤threading模块时, 
往往会定义⼀个新的⼦类class, 只要继承 threading.Thread 就可以了, 然后重写 run ⽅法
'''
import threading
import time

class MyThread(threading.Thread):
    # 重写run方法
    def run(self):
        for i in range(3):
            time.sleep(1)
            msg = 'I\'m' + self.name + ' @ ' + str(i)
            print(msg)

if __name__ == '__main__':
    m = MyThread()
    m.start()

'''
说明:
    python的threading.Thread类有⼀个run⽅法， ⽤于定义线程的功能函
    数， 可以在⾃⼰的线程类中覆盖该⽅法。 ⽽创建⾃⼰的线程实例后， 通
    过Thread类的start⽅法， 可以启动该线程 
    
    * 交给python虚拟机进⾏调度, 当该线程获得执⾏的机会时, 就会调⽤run⽅法执⾏线程。
'''

'''
测试结果:
I'mThread-1 @ 0
I'mThread-1 @ 1
I'mThread-1 @ 2
'''