# coding:utf-8

'''
@author = super_fazai
@File    : celery_utils.py
@connect : superonesfazai@gmail.com
'''

"""
celery常用函数
"""

from celery import Celery

__all__ = [
    'init_celery_app',          # 初始化一个celery对象
]

def init_celery_app(name='proxy_tasks',
                    broker='redis://127.0.0.1:6379',
                    backend='redis://127.0.0.1:6379/0',
                    celeryd_max_tasks_per_child=500) -> Celery:
    '''
    初始化一个celery对象
    :return:
    '''
    app = Celery(
        name,               # 创建一个celery实例, 名叫name
        broker=broker,      # 指定消息中间件，用redis
        backend=backend     # 指定存储用redis
    )
    app.conf.update(
        CELERY_TIMEZONE='Asia/Shanghai',                            # 指定时区, 默认是'UTC'
        CELERY_ACKS_LATE=True,
        CELERY_ACCEPT_CONTENT=['pickle', 'json'],                   # 注意: 'pickle'是一种Python特有的自描述的数据编码, 可序列化自定义对象
        CELERY_TASK_SERIALIZER='pickle',
        CELERY_RESULT_SERIALIZER='pickle',
        CELERYD_FORCE_EXECV=True,
        # CELERYD_HIJACK_ROOT_LOGGER=False,                         # 想要用自己的logger, 则设置为False
        CELERYD_MAX_TASKS_PER_CHILD=celeryd_max_tasks_per_child,    # 长时间运行Celery有可能发生内存泄露，可以像下面这样设置
        CELERY_TASK_RESULT_EXPIRES=60*60,                           # task result过期时间 单位秒
        BROKER_HEARTBEAT=0,)

    return app

