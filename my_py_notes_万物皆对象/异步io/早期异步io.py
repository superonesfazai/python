# coding:utf-8

'''
@author = super_fazai
@File    : 早期异步io.py
@connect : superonesfazai@gmail.com
'''

import asyncio

@asyncio.coroutine
def hello():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()