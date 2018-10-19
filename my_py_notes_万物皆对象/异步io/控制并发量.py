# coding:utf-8

'''
@author = super_fazai
@File    : 控制并发量.py
@connect : superonesfazai@gmail.com
'''

import aiohttp
from asyncio import get_event_loop, wait, Semaphore

NUMBERS = range(12)
URL = 'http://httpbin.org/get?a={}'
sema = Semaphore(3)

async def fetch_async(a):
    async with aiohttp.request('GET', URL.format(a)) as r:
        data = await r.json()
    return data['args']['a']

async def print_result(a):
    with (await sema):
        r = await fetch_async(a)
        print('fetch({}) = {}'.format(a, r))

loop = get_event_loop()
f = wait([print_result(num) for num in NUMBERS])
loop.run_until_complete(f)
loop.close()