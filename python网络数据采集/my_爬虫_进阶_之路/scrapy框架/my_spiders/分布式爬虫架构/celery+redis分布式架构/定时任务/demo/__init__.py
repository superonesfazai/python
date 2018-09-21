# coding:utf-8

'''
@author = super_fazai
@File    : __init__.py.py
@connect : superonesfazai@gmail.com
'''

from celery import Celery

app = Celery('demo')
app.config_from_object('demo.celery_config')

# 现在，让我们启动 Celery Worker 进程
# 在项目的根目录执行，即定时任务目录，非demo目录
# $ celery -A demo worker -l info

# 接着，启动 Celery Beat 进程，定时将任务发送到 Broker
# 还是在该目录执行
# $ celery beat -A demo