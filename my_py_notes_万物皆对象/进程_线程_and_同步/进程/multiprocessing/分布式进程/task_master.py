# coding:utf-8

'''
@author = super_fazai
@File    : task_master.py
@connect : superonesfazai@gmail.com
'''

"""
服务进程，服务进程负责启动Queue，把Queue注册到网络上，然后往Queue里面写入任务：
"""

import random
from queue import Queue, Empty
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = Queue()
# 接收结果的队列:
result_queue = Queue()

class QueueManager(BaseManager):
    pass

def return_task_queue():
    """
    返回发送任务队列
    :return:
    """
    global task_queue
    return task_queue

def return_result_queue():
    """
    返回接收结果队列
    :return:
    """
    global result_queue
    return result_queue

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=return_task_queue)
QueueManager.register('get_result_queue', callable=return_result_queue)

# 绑定端口5000, 设置验证码'abc':
queue_manager = QueueManager(address=('127.0.0.1', 5000), authkey='abc'.encode())
# 启动Queue:
queue_manager.start()
# 获得通过网络访问的Queue对象:
task = queue_manager.get_task_queue()
result = queue_manager.get_result_queue()

# 放几个任务进去:
for i in range(10):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)

# 从result队列读取结果:
print('Try get results...')
for i in range(10):
    try:
        r = result.get(timeout=5)
        print('Result: %s' % r)
    except Empty:
        print('result queue is empty.')

# 关闭:
queue_manager.shutdown()
print('master exit.')

"""
Put task 3511...
Put task 7456...
Put task 9804...
Put task 127...
Put task 6369...
Put task 3547...
Put task 6146...
Put task 199...
Put task 5588...
Put task 2488...
Try get results...
Result: 3511 * 3511 = 12327121
Result: 7456 * 7456 = 55591936
Result: 9804 * 9804 = 96118416
Result: 127 * 127 = 16129
Result: 6369 * 6369 = 40564161
Result: 3547 * 3547 = 12581209
Result: 6146 * 6146 = 37773316
Result: 199 * 199 = 39601
Result: 5588 * 5588 = 31225744
Result: 2488 * 2488 = 6190144
master exit.
"""