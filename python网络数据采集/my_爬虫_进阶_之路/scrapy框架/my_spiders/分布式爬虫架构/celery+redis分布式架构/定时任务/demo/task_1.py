# coding:utf-8

'''
@author = super_fazai
@File    : task_1.py
@Time    : 2018/7/1 17:37
@connect : superonesfazai@gmail.com
'''
import time
from . import app

@app.task
def add(x, y):
    time.sleep(2)

    return x + y