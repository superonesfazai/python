# coding:utf-8

'''
@author = super_fazai
@File    : 新线程协程.py
@connect : superonesfazai@gmail.com
'''

from threading import Thread
from fzutils.spider.async_always import *

def start_loop(loop):
    set_event_loop(loop)
    loop.run_forever()

async def do_some_work(x):
    print('Waiting {}'.format(x))
    await async_sleep(x)
    print('Done after {}s'.format(x))

new_loop = new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()

run_coroutine_threadsafe(do_some_work(6), new_loop)
run_coroutine_threadsafe(do_some_work(4), new_loop)

t.join()