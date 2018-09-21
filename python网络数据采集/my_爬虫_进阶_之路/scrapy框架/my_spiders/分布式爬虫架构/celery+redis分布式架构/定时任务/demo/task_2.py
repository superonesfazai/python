# coding:utf-8

'''
@author = super_fazai
@File    : task_2.py
@connect : superonesfazai@gmail.com
'''

import time
from . import app

@app.task
def multiply(x, y):
    time.sleep(2)
    return x * y