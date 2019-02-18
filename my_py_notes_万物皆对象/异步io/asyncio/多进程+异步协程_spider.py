# coding:utf-8

'''
@author = super_fazai
@File    : 多进程+异步协程_spider.py
@connect : superonesfazai@gmail.com
'''

import asyncio
import time
import random
import etree
from asyncio import Semaphore
from aiohttp import ClientSession,TCPConnector
import urllib.request as request
from multiprocessing.pool import Pool

url = 'http://www.quanjing.com/creative/SearchCreative.aspx?id=7'

def get_pic_src(url:str)->list:
    response = request.urlopen(url)
    wb_data = response.read()
    html = etree.HTML(wb_data)
    pic_urls = html.xpath('//a[@class="item lazy"]/img/@src')

    return pic_urls

async def download(session:ClientSession,url:str,name:str,sem:Semaphore,suffix:str='jpg'):
    path = '.'.join([name,suffix])
    async with sem:
        async with session.get(url) as response:
            wb_data = await response.read()
            with open(path,'wb') as f:
                f.write(wb_data)

async def run_coroutine_crawler(pic_urls:list,concurrency:int):
    # 异步协程爬虫,最大并发请求数concurrency
    tasks = []
    sem = Semaphore(concurrency)
    conn =TCPConnector(limit=concurrency)
    async with ClientSession(connector=conn) as session:
        for i in pic_urls:
            ts = str(int(time.time() * 10000)) + str(random.randint(1, 100000))
            tasks.append(asyncio.create_task(download(session,i,ts,sem)))
        start = time.time()
        await asyncio.gather(*tasks)
        end = time.time()
        print(u'下载完成,%d张图片,耗时:%.2fs' % (len(pic_urls), (end - start)))

def allot(pic_urls:list,n:int)->list:
    # 根据给定的组数，分配url给每一组
    _len = len(pic_urls)
    base = int(_len / n)
    remainder = _len % n
    groups = [pic_urls[i * base:(i + 1) * base] for i in range(n)]
    remaind_group = pic_urls[n * base:]
    for i in range(remainder):
        groups[i].append(remaind_group[i])

    return [i for i in groups if i]

def _coroutine_crawler(pic_urls:list,concurrency:int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_coroutine_crawler(pic_urls, concurrency))
    loop.close()

def mixed_process_coroutine_crawler(processors:int,concurrency:int):
    """
    main
    :param processors:
    :param concurrency:
    :return:
    """
    pool = Pool(processors)
    pic_urls = get_pic_src(url)
    url_groups = allot(pic_urls, processors)
    for group in url_groups:
        pool.apply_async(_coroutine_crawler, args=(group, concurrency))
    pool.close()
    pool.join()

mixed_process_coroutine_crawler(4, 50)