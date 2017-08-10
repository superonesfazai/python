# coding = utf-8

'''
@author = super_fazai
@File    : ⽤FIFO队列实现上述⽣产者与消费者问题.py
@Time    : 2017/8/9 17:56
@connect : superonesfazai@gmail.com
'''

import threading
import time

# python2中
# from Queue import Queue
# python3中
from queue import Queue

class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            if queue.qsize() < 1000:
                for i in range(100):
                    count = count +1
                    msg = '⽣成产品'+str(count)
                    queue.put(msg)
                    print(msg)
            time.sleep(0.5)

class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize() > 100:
                for i in range(3):
                    msg = self.name + '消费了 '+queue.get()
                    print(msg)
            time.sleep(1)

if __name__ == '__main__':
    queue = Queue()
    for i in range(500):
        queue.put('初始产品'+str(i))
    for i in range(2):
        p = Producer()
        p.start()
    for i in range(5):
        c = Consumer()
        c.start()