# coding:utf-8

'''
@author = super_fazai
@File    : demo2.py
@connect : superonesfazai@gmail.com
'''

"""
在gevent里面，上下文切换是通过yielding来完成的. 
在下面的例子里， 我们有两个上下文，通过调用gevent_sleep(0)，它们各自yield向对方。
"""

import gevent
from gevent import sleep as gevent_sleep

def foo():
    print('Running in foo')
    gevent_sleep(0)
    print('Explicit context switch to foo again')

def bar():
    print('Explicit context to bar')
    gevent_sleep(0)
    print('Implicit context switch back to bar')

gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar),
])

"""
Running in foo
Explicit context to bar
Explicit context switch to foo again
Implicit context switch back to bar
"""