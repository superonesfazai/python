# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2018/5/19 15:05
@connect : superonesfazai@gmail.com
'''

from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',      # 这个配置文件中对象名, broker, backend, 必须有，才能正常运行获取redis结果
    backend='redis://localhost:6379/0'
)

app.conf.update(
    CELERY_ACKS_LATE=True,
    CELERY_ACCEPT_CONTENT=['pickle', 'json'],
    CELERYD_FORCE_EXECV=True,
    CELERYD_MAX_TASKS_PER_CHILD=500,
    BROKER_HEARTBEAT=0,
)

@app.task
def add(x, y):
    return x + y


