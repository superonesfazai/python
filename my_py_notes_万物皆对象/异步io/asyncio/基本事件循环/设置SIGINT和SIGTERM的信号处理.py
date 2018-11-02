# coding:utf-8

'''
@author = super_fazai
@File    : 设置SIGINT和SIGTERM的信号处理.py
@connect : superonesfazai@gmail.com
'''

"""
注册信号处理程序SIGINT并SIGTERM使用该AbstractEventLoop.add_signal_handler()方法
"""

from asyncio import get_event_loop
import functools
import os
import signal

def ask_exit(signame):
    print("got signal %s: exit" % signame)
    loop.stop()

loop = get_event_loop()
for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(
        getattr(signal, signame),
        functools.partial(ask_exit, signame))

print("Event loop running forever, press Ctrl+C to interrupt.")
print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
try:
    loop.run_forever()
finally:
    loop.close()