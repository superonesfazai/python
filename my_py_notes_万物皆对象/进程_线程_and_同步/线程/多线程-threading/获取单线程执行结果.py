# coding:utf-8

'''
@author = super_fazai
@File    : 获取单线程执行结果.py
@connect : superonesfazai@gmail.com
'''

from threading import (
    Thread,)
import sys
from queue import Queue

"""
方法1: 可采用类包装线程的方法来获取线程返回值
"""

class TaskObj(Thread):
    """
    task 对象(可以通过继承Thread对象来, 重写run方法来执行特定的功能, 重写get_result来获取线程执行结果!)
    """
    def __init__(self, func, args=()):
        super(TaskObj, self).__init__()
        self.func = func
        self.args = args
        self.res = None     # Thread结果

    def run(self):
        self.res = self.func(*self.args)

    def _get_result(self):
        Thread.join(self)  # 等待线程执行完毕
        try:
            return self.res
        except Exception:
            return None

def add(a, b):
    return a + b

def method_1():
    '''方法1: 可采用类包装线程的方法来获取线程返回值'''
    list = [23, 89]
    # 创建4个线程
    for i in range(4):
        task = TaskObj(add, (list[0], list[1]))
        task.start()  # 开启该线程
        print(task._get_result())


"""
方法2: 用一个队列存放线程处理结果，再进行取出(这种做法比较主流)
"""

q = Queue()

def worker1(x, y):
    func_name = sys._getframe().f_code.co_name
    print("%s run ..." % func_name)
    q.put((x + y, func_name))

def worker2(x, y):
    func_name = sys._getframe().f_code.co_name
    print("%s run ...." % func_name)
    q.put((x - y, func_name))

def method_2():
    '''方法2: 用一个队列存放线程处理结果，再进行取出(这种做法比较主流)'''
    result = list()
    t1 = Thread(target=worker1, name='thread1', args=(10, 5,))
    t2 = Thread(target=worker2, name='thread2', args=(20, 1,))
    t1.start()
    t2.start()
    # 将线程设置为守护线程
    # t1.setDaemon(True)
    # t2.setDaemon(True)
    t1.join()   # 阻塞
    t2.join()
    while not q.empty():
        result.append(q.get())

    _ = "%s 's return value is : %s"
    for item in result:
        if item[1] == worker1.__name__:
            print(_ % (item[1], item[0]))

        elif item[1] == worker2.__name__:
            print(_ % (item[1], item[0]))

if __name__ == "__main__":
    # method_1()
    method_2()

