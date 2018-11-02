# coding:utf-8

'''
@author = super_fazai
@File    : 优先级队列.py
@connect : superonesfazai@gmail.com
'''

"""
异步优先级队列: 用于控制优先级
"""

import random
import aiohttp
from asyncio import (
    Semaphore,
    get_event_loop,
    wait,
    PriorityQueue,
    ensure_future,
)

NUMBERS = random.sample(range(100), 7)
URL = 'http://httpbin.org/get?a={}'
sema = Semaphore(3)

async def fetch_async(a):
    async with aiohttp.request('GET', URL.format(a)) as r:
        data = await r.json()
    return data['args']['a']

async def collect_result(a):
    with (await sema):
        return await fetch_async(a)

async def produce(queue):
    for num in NUMBERS:
        print('producing {}'.format(num))
        item = (num, num)
        await queue.put(item)

async def consume(queue):
    while 1:
        item = await queue.get()
        num = item[0]
        rs = await collect_result(num)
        print('consuming {}...'.format(rs))
        queue.task_done()

async def run():
    queue = PriorityQueue()
    consumer = ensure_future(consume(queue))
    await produce(queue)
    await queue.join()
    consumer.cancel()

loop = get_event_loop()
loop.run_until_complete(run())
loop.close()

