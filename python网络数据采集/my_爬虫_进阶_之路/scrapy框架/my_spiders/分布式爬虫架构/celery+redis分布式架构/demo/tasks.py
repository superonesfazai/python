# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

"""
分布式启动:
celery -A tasks worker -P eventlet -c 300 -l info 

查看所有已注册的task
celery -A {xxx} inspect registered
"""

import celery
from celery.utils.log import get_task_logger
from fzutils.celery_utils import init_celery_app
from fzutils.spider.async_always import *

CELERY_TASK_BASE_NAME = 'tasks'
app = init_celery_app(
    name=CELERY_TASK_BASE_NAME,     # name必须指定, 否则会收到其他同名的celery task
)
# 最佳实践是在模块的顶层，为你的所有任务创建一个共用的logger
logger = get_task_logger(__name__)

@app.task(name=CELERY_TASK_BASE_NAME + '.add', bind=True)
def add(x, y):
    '''创建一个可被celery调度的任务'''
    return x + y

'''绑定任务'''
# 一个任务被绑定: 意味着这个任务的第一个参数是celery app实例(即self)和python中的绑定方法一样：
# 绑定任务用于尝试重新执行任务(使用app.Task.retry()), 绑定了任务就可以访问当前请求的任务信息 和 任何你添加到指定任务基类中的方法。
@app.task(name=CELERY_TASK_BASE_NAME+'.add_2', bind=True)
def add_2(self, x, y):
    logger.info(self.request.id)

@app.task(name=CELERY_TASK_BASE_NAME + '.test_async', bind=True)
def test_async(self):
    '''
    原生异步测试
    :return:
    '''
    def _get_args():
        return []

    async def aa():
        logger.info('*' * 10)
        await async_sleep(2)

        return True

    logger.info('*' * 100)
    logger.info(self.request.id)
    logger.info(str(self.request.headers))

    loop = new_event_loop()
    args = _get_args()
    res = loop.run_until_complete(aa)

    return res

'''任务继承'''
# task装饰器的"base"关键字参数用于指定任务的基类：
# class MyTask(celery.Task):
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print('{0!r} failed: {1!r}'.format(task_id, exc)
#
# @app.task(base=MyTask)
# def add_3(x, y):
#     raise KeyError()

'''名字'''
# 每个任务都必须拥有一个唯一的名字，如果你没有指定"name"关键字参数，将会用函数名产生一个名字。
# >>> @app.task(name='sum-of-two-numbers')
# >>> def add(x, y):
# ...     return x + y
#
# >>> add.name
# 'sum-of-two-numbers'
# * 最佳实践是使用模块名作为一个命名空间，这样任务名就不会与另外一个模块中已经存在的同名任务冲突
# >>> @app.task(name='tasks.add')
# >>> def add(x, y):
# ...     return x + y





