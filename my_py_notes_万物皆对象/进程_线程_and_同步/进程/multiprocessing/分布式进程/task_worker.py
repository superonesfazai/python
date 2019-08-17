# coding:utf-8

'''
@author = super_fazai
@File    : task_worker.py
@connect : superonesfazai@gmail.com
'''

import time
from queue import Empty, Queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register(
    typeid='get_task_queue')
QueueManager.register(
    typeid='get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)

# 端口和验证码注意保持与task_master.py设置的完全一致:
queue_manager = QueueManager(address=(server_addr, 5000), authkey='abc'.encode())
queue_manager.connect()

# 获取Queue的对象:
task = queue_manager.get_task_queue()
result = queue_manager.get_result_queue()

# 从task队列取任务,并把结果写入result队列:
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except Empty:
        print('task queue is empty.')

# 处理结束:
print('worker exit.')

"""
Connect to server 127.0.0.1...
run task 3511 * 3511...
run task 7456 * 7456...
run task 9804 * 9804...
run task 127 * 127...
run task 6369 * 6369...
run task 3547 * 3547...
run task 6146 * 6146...
run task 199 * 199...
run task 5588 * 5588...
run task 2488 * 2488...
worker exit.
"""