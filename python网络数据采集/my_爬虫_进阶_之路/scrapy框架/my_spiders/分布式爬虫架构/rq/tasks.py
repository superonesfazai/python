# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

from rq.decorators import job
from time import sleep

@job('low', connection='redis://127.0.0.1:6379/0', timeout=5)
def add(x, y):
    return x + y

job = add.delay(3, 4)
sleep(1)
print(job.result)
