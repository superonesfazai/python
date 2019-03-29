# coding:utf-8

'''
@author = super_fazai
@File    : aio_huayu_spider.py
@Time    : 2018/3/23 14:41
@connect : superonesfazai@gmail.com
'''

import time
from operator import itemgetter

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.async_always import *

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
            try:
                sort = Selector(text=_).css('span.book em a::text').extract_first().__str__()
                book_name = Selector(text=_).css('span.book a::attr("title")').extract()[1].__str__()
                book_link = 'http://huayu.baidu.com' + Selector(text=_).css('span.book a::attr("href")').extract()[1].__str__()
                book_click_number = Selector(text=_).css('span.click::text').extract_first().__str__()
                assert book_click_number is not None, 'book_click_number为None!'
                author = Selector(text=_).css('span.author a::attr("title")').extract_first().__str__()
            except AssertionError:
                continue

            one_data = {
                'sort': sort,
                'book_name': book_name,
                'book_link': book_link,
                'book_click_number': int(book_click_number),
                'author': author
            }
            cleaned_data.append(one_data)

            # print(sort, ' ', book_name, ' ', book_link, ' ', book_click_number, ' ', author)

    cleaned_data = sorted(cleaned_data, key=itemgetter('book_click_number'))   # 按点击数进行排序从小到大
    for item in reversed(cleaned_data):
        print('{sort:10s} {book_name:20s} {book_link:50s} {book_click_number:10d} {author:10s}'.format(**item))

    print('总计小说本数:', len(cleaned_data))

    return cleaned_data

async def main(loop):
    tasks = []
    for page_num in range(1, 18):
        print('create task page_num: {}'.format(page_num))
        tasks.append(loop.create_task(_get_one_page(
            page_num=page_num,
        )))

    all_res = await async_wait_tasks_finished(tasks=tasks)
    await deal_with_result(all_res)
    # print(all_result)

async def _get_one_page(page_num) -> str:
    """
    获取单页html
    :param page_num:
    :return:
    """
    headers = get_base_headers()
    headers.update({
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    url = 'http://huayu.baidu.com/rank/c0/u14/p{0}/v0/ALL.html'.format(page_num)
    # 成功率高于unblock_request且更快!
    body = await AioHttp.aio_get_url_body(
        url=url,
        headers=headers,
        ip_pool_type=tri_ip_pool,
        timeout=12,
        num_retries=1,)

    # body = await unblock_request(
    #     url=url,
    #     headers=headers,
    #     ip_pool_type=tri_ip_pool,
    #     timeout=12,
    #     num_retries=1,)

    print('[{}] page_num: {}'.format(
        '+' if body != '' else '-',
        page_num,
    ))

    return body

start_time = time.time()
loop = get_event_loop()
loop.run_until_complete(main(loop))
end_time = time.time()
print('用时: ', end_time-start_time)

