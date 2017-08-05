# encoding: utf-8

'''
测试环境: python2.7
在pyhton3以上不支持模块Queue了
'''

from Queue import Queue
import random
import threading
import time


class Producer(threading.Thread):
    """
    Producer thread
    """
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):
            print("%s: %s is producing %d to the queue!" % (time.ctime(), self.getName(), i))
            self.data.put(i)
            time.sleep(random.randrange(10) / 5)
        print("%s: %s finished!" % (time.ctime(), self.getName()))


class Consumer(threading.Thread):
    """
    Consumer thread
    """
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):
            val = self.data.get()
            print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val))
            time.sleep(random.randrange(10))
        print("%s: %s finished!" % (time.ctime(), self.getName()))


def main():
    """
    Main thread
    :return:
    """
    queue = Queue()
    producer = Producer('Pro.', queue)
    consumer = Consumer('Con.', queue)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
    print('All threads terminate!')


if __name__ == '__main__':
    main()

# 本程序是比较经典的生产者和消费者模型，运行结果：
'''
测试结果如下:
Sat Aug  5 17:13:10 2017: Pro. is producing 0 to the queue!
Sat Aug  5 17:13:10 2017: Con. is consuming. 0 in the queue is consumed!
Sat Aug  5 17:13:11 2017: Pro. is producing 1 to the queue!
Sat Aug  5 17:13:12 2017: Pro. is producing 2 to the queue!
Sat Aug  5 17:13:12 2017: Pro. is producing 3 to the queue!
Sat Aug  5 17:13:13 2017: Pro. is producing 4 to the queue!
Sat Aug  5 17:13:14 2017: Pro. finished!
Sat Aug  5 17:13:15 2017: Con. is consuming. 1 in the queue is consumed!
Sat Aug  5 17:13:23 2017: Con. is consuming. 2 in the queue is consumed!
Sat Aug  5 17:13:26 2017: Con. is consuming. 3 in the queue is consumed!
Sat Aug  5 17:13:30 2017: Con. is consuming. 4 in the queue is consumed!
Sat Aug  5 17:13:34 2017: Con. finished!
All threads terminate!
'''