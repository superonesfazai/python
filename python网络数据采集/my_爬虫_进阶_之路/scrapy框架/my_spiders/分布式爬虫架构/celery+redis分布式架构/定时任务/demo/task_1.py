# coding:utf-8

'''
@author = super_fazai
@File    : task_1.py
@connect : superonesfazai@gmail.com
'''
import time
from . import app

@app.task
def add(x, y):
    time.sleep(2)

    return x + y