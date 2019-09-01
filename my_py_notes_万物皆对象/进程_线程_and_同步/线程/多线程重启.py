# coding:utf-8

'''
@author = super_fazai
@File    : 多线程重启.py
@connect : superonesfazai@gmail.com
'''

"""
python 多线程程序运行中，会出现由于异常而导致某线程停止的情况，为了保证程序的稳定运行，需要自动重启down掉的线程.
python Threading类有一个setName()的方法，可以为线程设置名字。
threading.enumerate()可以获取当前的线程对象。

自动重启线程的思路如下：
1.使用setName（）每个线程设置名字；
2.在初始化运行时使用threading.enumerate()获取当前所有线程对象，保存为初始线程组；
3.隔一段时间使用threading.enumerate()获取当前所有线程对象，与初始线程组对比，如果某个name缺失，则重新start。
"""

from fzutils.thread_utils import Thread
from fzutils.spider.async_always import *

def print_num(num):
    sleep(5.)
    print(num)

class TestThread(Thread):
    def __init__(self, args: (list, tuple)=()):
        super(TestThread, self).__init__()
        self.args = args

    def run(self):
        sleep(5.)
        print(self.args[0])

if __name__ == '__main__':
    # 任务信息列表 eg: [{'thread_name': 'thread_task:print_ip:is_class_False:21113cf4-cc69-11e9-bdef-68fef70d1e6e', 'func_args': [xxx,]}, 'is_class': False]
    # 存储所有需要监控并重启的初始化线程对象list
    need_to_be_monitored_thread_tasks_info_list = []

    tasks = []
    # 函数类型的
    for num in range(0, 3):
        func_args = [
            num,
        ]
        t = Thread(
            target=print_num,
            args=func_args)
        thread_task_name = 'thread_task:{}:{}'.format(
            'print_ip',
            get_uuid1())
        t.setName(thread_task_name)
        tasks.append(t)
        need_to_be_monitored_thread_tasks_info_list.append({
            'func_name': print_num,
            'thread_name': thread_task_name,
            'func_args': func_args,
            'is_class': False,                  # 是否是类, 函数为False
        })

    # 继承自Thread的类
    for num in range(3, 4):
        func_args = [
            num,
        ]
        task = TestThread(args=func_args)
        thread_task_name = 'thread_task:{}:{}'.format(
            'TestThread',
            get_uuid1(),)
        task.setName(thread_task_name)
        tasks.append(task)
        need_to_be_monitored_thread_tasks_info_list.append({
            'func_name': TestThread,
            'thread_name': thread_task_name,
            'func_args': func_args,
            'is_class': True,
        })

    for t in tasks:
        t.start()

    # pprint(need_to_be_monitored_thread_tasks_info_list)

    # 用来检测是否有线程down并重启down线程
    check_thread_task = Thread(
        target=check_thread_tasks_and_restart,
        args=(
            need_to_be_monitored_thread_tasks_info_list,
            6,
        ))
    check_thread_task.setName('thread_task:check_thread_task_and_restart')
    check_thread_task.start()