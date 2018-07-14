# coding:utf-8

'''
@author = super_fazai
@File    : fz_aiohttp.py
@Time    : 2018/7/14 14:45
@connect : superonesfazai@gmail.com
'''

import asyncio
import aiohttp
import re
import gc
import time
from random import randint

from ..ip_pools import MyIpPools
from ..internet_utils import get_random_pc_ua

class MyAiohttp(object):
    def __init__(self, max_tasks=10):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.max_tasks = max_tasks  # 接口请求进程数
        self.queue = asyncio.Queue(loop=self.loop)  # 接口队列
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'superonesfazai.github.io',
            # 'if-modified-since': get_right_time(),
            'User-Agent': get_random_pc_ua(),      # 随机一个请求头
        }

    @classmethod    # 注意timeout不是越长越好，测试发现10左右成功率较高
    async def aio_get_url_body(self, url, headers, params=None, timeout=10, num_retries=10):
        '''
        异步获取url的body(简略版)
        :param url:
        :param headers:
        :param params:
        :param had_proxy:
        :param num_retries: 出错重试次数
        :return:
        '''
        proxy = await self.get_proxy()

        # 连接池不能太大, < 500
        conn = aiohttp.TCPConnector(verify_ssl=True, limit=150, use_dns_cache=True)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                async with session.get(url=url, headers=headers, params=params, proxy=proxy, timeout=timeout) as r:
                    result = await r.text(encoding=None)
                    result = await self.wash_html(result)
                    # print('success')
                    return result
            except Exception as e:
                # print('出错:', e)
                if num_retries > 0:
                    # 如果不是200就重试，每次递减重试次数
                    return await self.aio_get_url_body(url=url, headers=headers, params=params, num_retries=num_retries - 1)
                else:
                    print('异步获取body失败!')
                    return ''

    @classmethod
    async def wash_html(self, body):
        '''
        异步清洗html
        :param body:
        :return:
        '''
        body = re.compile('\t').sub('', body)
        body = re.compile('  ').sub('', body)
        body = re.compile('\r\n').sub('', body)
        body = re.compile('\n').sub('', body)

        return body

    @classmethod
    async def get_proxy(self):
        '''
        异步获取proxy
        :return: 格式: 'http://ip:port'
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        proxy = ip_object._get_random_proxy_ip()    # 失败返回False

        return proxy

    async def run(self):
        url = 'https://superonesfazai.github.io/'

        # 对比发现 总数 越大，aiohttp的效率就比requests更高(100个 aiohttp:35s, requests:43s)
        tasks = [self.loop.create_task(self.aio_get_url_body(url=url, headers=self.headers)) for _ in range(self.max_tasks)]
        finished_job, unfinished_job = await asyncio.wait(tasks)  # tasks是待执行的异步函数的list eg:[hello(), hello(), ...] 进行并行执行
        all_result = [r.result() for r in finished_job]
        # print(all_result)

        return all_result

    def __del__(self):
        self.loop.close()
        gc.collect()

# if __name__ == '__main__':
#     start_time = time.time()
#     loop = asyncio.get_event_loop()
#     my_aiohttp = MyAiohttp(max_tasks=1)
#     result = loop.run_until_complete(my_aiohttp.run())
#     print(result)
#     end_time = time.time()
#     print('用时: ', end_time - start_time)
#     try: del my_aiohttp
#     except: pass
#     loop.close()
