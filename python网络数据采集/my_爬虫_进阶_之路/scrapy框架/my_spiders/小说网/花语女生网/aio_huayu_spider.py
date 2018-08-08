# coding:utf-8

'''
@author = super_fazai
@File    : aio_huayu_spider.py
@Time    : 2018/3/23 14:41
@connect : superonesfazai@gmail.com
'''

import asyncio
from aiohttp.client_exceptions import (
    ClientHttpProxyError,
    ClientOSError,
    ClientResponseError,)
from asyncio import TimeoutError
import time
from pprint import pprint
from scrapy.selector import Selector

from fzutils.spider.fz_aiohttp import MyAiohttp

def get_right_time():
    a = time.ctime().split()
    a[0] = a[0] + ','
    b = [a[0], a[2], a[1], a[4], a[3]]

    return ' '.join(b) + ' GMT'

print(get_right_time())

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'huayu.baidu.com',
    'if-modified-since': get_right_time(),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',      # 随机一个请求头
}

async def deal_with_result(result):
    '''
    规范处理数据
    :param result:
    :return:
    '''
    cleaned_data = []
    for item in result:
        if isinstance(item, bool):
            continue
        for _ in list(Selector(text=item).css('div.table_con ul li').extract()):
            if isinstance(_, bool):
                continue
            sort = Selector(text=_).css('span.book em a::text').extract_first().__str__()
            book_name = Selector(text=_).css('span.book a::attr("title")').extract()[1].__str__()
            book_link = 'http://huayu.baidu.com' + Selector(text=_).css('span.book a::attr("href")').extract()[1].__str__()
            book_click_number = Selector(text=_).css('span.click::text').extract_first().__str__()
            author = Selector(text=_).css('span.author a::attr("title")').extract_first().__str__()

            one_data = {
                'sort': sort,
                'book_name': book_name,
                'book_link': book_link,
                'book_click_number': int(book_click_number),
                'author': author
            }
            cleaned_data.append(one_data)

            # print(sort, ' ', book_name, ' ', book_link, ' ', book_click_number, ' ', author)
    from operator import itemgetter
    cleaned_data = sorted(cleaned_data, key=itemgetter('book_click_number'))   # 按点击数进行排序从小到大
    for item in reversed(cleaned_data):
        print(item['sort'], ' ', item['book_name'], ' ', item['book_link'], ' ', item['book_click_number'], ' ', item['author'])

    print('总计小说本数:', len(cleaned_data))

    return cleaned_data

async def main(loop):
    tasks = []
    for _ in range(1, 18):
        url = 'http://huayu.baidu.com/rank/c0/u14/p{0}/v0/ALL.html'.format(str(_))
        tasks.append(loop.create_task(MyAiohttp.aio_get_url_body(url=url, headers=headers, params=None, timeout=12, num_retries=8)))
    finished, unfinished = await asyncio.wait(tasks)
    all_result = [r.result() for r in finished]
    await deal_with_result(all_result)
    # print(all_result)

start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
end_time = time.time()
print('用时: ', end_time-start_time)

