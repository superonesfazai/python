# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2018/5/19 15:05
@connect : superonesfazai@gmail.com
'''

from celery import Celery
from celery.utils.log import get_task_logger
import celery

def init_celery_app():
    '''
    初始化一个celery对象
    :return:
    '''
    app = Celery(
        'tasks',        # 创建一个celery实例, 名叫'task'
        broker='redis://127.0.0.1:6379',  # 指定消息中间件，用redis
        backend='redis://127.0.0.1:6379/0'  # 指定存储用redis
    )

    app.conf.update(
        CELERY_TIMEZONE='Asia/Shanghai',    # 指定时区, 默认是'UTC'
        # CELERY_ENABLE_UTC=True,
        CELERY_ACKS_LATE=True,
        CELERY_ACCEPT_CONTENT=['pickle', 'json'],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERYD_FORCE_EXECV=True,
        CELERYD_MAX_TASKS_PER_CHILD=500,
        BROKER_HEARTBEAT=0,
    )

    return app

app = init_celery_app()

# 创建一个被@app.task装饰的函数add, 即创建一个可被celery调度的任务
@app.task
def add(x, y):
    return x + y

'''绑定任务'''
# 一个任务被绑定: 意味着这个任务的第一个参数是celery app实例(即self)和python中的绑定方法一样：
# 绑定任务用于尝试重新执行任务(使用app.Task.retry()), 绑定了任务就可以访问当前请求的任务信息 和 任何你添加到指定任务基类中的方法。
logger = get_task_logger(__name__)  # 最佳实践是在模块的顶层，为你的所有任务创建一个共用的logger。

@app.task(bind=True)
def add_2(self, x, y):
    logger.info(self.request.id)

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





