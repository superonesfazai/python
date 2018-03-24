# coding:utf-8

'''
@author = super_fazai
@File    : demo_2.py
@Time    : 2018/3/23 10:17
@connect : superonesfazai@gmail.com
'''

"""
aiohttp

aiohttp 3.0 的重试机制
"""

from my_ip_pools import MyIpPools
from my_requests import MyRequests
import re

import aiohttp
import asyncio
from aiohttp.client_exceptions import ClientHttpProxyError, ClientOSError, ClientResponseError
from asyncio import TimeoutError
import time
from random import randint
from pprint import pprint

def get_right_time():
    '''
    得到需求时间str
    :return: 格式为: 'Sat, 06 Jan 2018 06:35:53 GMT'
    '''
    a = time.ctime().split()
    a[0] = a[0] + ','
    b = [a[0], a[2], a[1], a[4], a[3]]

    return ' '.join(b) + ' GMT'

# print(get_right_time())

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'superonesfazai.github.io',
    # 'if-modified-since': get_right_time(),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',      # 随机一个请求头
}

async def wash_html(body):
    body = re.compile('\t').sub('', body)
    body = re.compile('  ').sub('', body)
    body = re.compile('\r\n').sub('', body)
    body = re.compile('\n').sub('', body)

    return body

async def get_proxy():
    # 设置代理ip
    ip_object = MyIpPools()
    ip_list = ip_object.get_proxy_ip_from_ip_pool()['http']
    proxy = ip_list[randint(0, len(ip_list) - 1)]

    return proxy

async def aio_get_url_body(url, headers, params=None, timeout=12, num_retries=8):
    '''
    异步获取url的body
    :param url:
    :param headers:
    :param params:
    :param had_proxy:
    :param num_retries: 出错重试次数
    :return:
    '''
    # 设置代理ip
    # ip_object = MyIpPools()
    # ip_list = ip_object.get_proxy_ip_from_ip_pool()['http']
    # proxy = ip_list[randint(0, len(ip_list) - 1)]
    proxy = await get_proxy()

    # 连接池不能太大, < 500
    conn = aiohttp.TCPConnector(verify_ssl=True, limit=150, use_dns_cache=True)
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            async with session.get(url=url, headers=headers, params=params, proxy=proxy, timeout=timeout) as r:
                result = await r.text(encoding=None)
                result = await wash_html(result)
                print('success')
                return result
        except Exception as e:
            # print('出错:', e)
            if num_retries > 0:
                # 如果不是200就重试，每次递减重试次数
                return await aio_get_url_body(url=url, headers=headers, params=params, num_retries=num_retries-1)

async def main(loop):
    url = 'https://superonesfazai.github.io/'
    tasks = [loop.create_task(aio_get_url_body(url=url, headers=headers)) for _ in range(100)]
    # tasks = []
    # for _ in range(100):    # 对比发现 总数 越大，aiohttp的效率就比requests更高(100个 aiohttp:35s, requests:43s)
    #     tasks.append(loop.create_task(aio_get_url_body(url=url, headers=headers, params=None)))
    finished_job, unfinished_job = await asyncio.wait(tasks)    # tasks是待执行的异步函数的list eg:[hello(), hello(), ...] 进行并行执行
    # all_result = [r.result() for r in finished_job]
    # print(all_result)

start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
end_time = time.time()
print('用时: ', end_time-start_time)

def test_requests():
    url = 'https://superonesfazai.github.io/'
    start_time = time.time()
    for _ in range(200):
        body = MyRequests.get_url_body(url=url, headers=headers)
        if body != '':
            print('success')
        else:
            print(body)

    end_time = time.time()
    print('requests用时:', end_time-start_time)

test_requests()

'''
如果要获取网页返回的结果, 我们可以在 job() 中 return 个结果出来
然后再在 finished, unfinished = await asyncio.wait(tasks) 收集完成的结果
这里它会返回完成的和没完成的, 我们关心的都是完成的, 而且 await 也确实是等待都完成了才返回. 真正的结果被存放在了 result() 里面.
'''