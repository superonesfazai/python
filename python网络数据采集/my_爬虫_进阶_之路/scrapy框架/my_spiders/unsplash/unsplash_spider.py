# coding:utf-8

'''
@author = super_fazai
@File    : unsplash_spider.py
@connect : superonesfazai@gmail.com
'''

"""
unsplash 图片网爬虫(https://unsplash.com/)
"""

from gc import collect
from fzutils.spider.crawler import AsyncCrawler
from fzutils.spider.async_always import *

class UnsplashSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(self, *params, **kwargs)

    async def _get_phone_headers(self):
        return {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_phone_ua(),
            'viewport-width': '400',
            'accept': '*/*',
            'referer': 'https://unsplash.com/',
            'authority': 'unsplash.com',
            'dpr': '2',
        }

    async def _get_one_page_info(self, page_num=1):
        '''
        获取一页页面的信息
        :return:
        '''
        params = (
            ('page', str(page_num)),
            ('per_page', '12'),
            ('order_by', 'latest'),
        )
        url = 'https://unsplash.com/napi/photos'
        data = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_phone_headers(), params=params), default_res=[])
        # print(data)

        return data

    async def _get_all_latest_pics_info(self):
        '''
        获取最近的所有图片信息
        :return:
        '''
        _ = []
        for base in range(1, 100, self.concurrency):
            tasks = []
            for page_num in range(base, base+self.concurrency, 1):
                print('create task {}...'.format(page_num))
                tasks.append(self.loop.create_task(self._get_one_page_info(page_num=page_num)))

            all_res = await async_wait_tasks_finished(tasks=tasks)
            for item in all_res:
                if item != []:
                    _ += item

        return _

    async def _fck_run(self):
        latest_pics_list = await self._get_all_latest_pics_info()
        pprint(latest_pics_list)
        print('总个数: {}'.format(len(latest_pics_list)))

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = UnsplashSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

