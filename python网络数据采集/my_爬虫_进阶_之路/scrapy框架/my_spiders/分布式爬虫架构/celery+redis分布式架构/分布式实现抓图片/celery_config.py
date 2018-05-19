# coding:utf-8

'''
@author = super_fazai
@File    : celery_config.py.py
@Time    : 2018/5/19 17:53
@connect : superonesfazai@gmail.com
'''

"""
celery配置
"""

from celery import Celery

app = Celery(
    'celery_config',
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0',
    include=['spider']
)

