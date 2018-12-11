# coding:utf-8

'''
@author = super_fazai
@File    : sdk_cn_spider.py
@connect : superonesfazai@gmail.com
'''

"""
sdk.cn 爬虫
"""

from gc import collect
from fzutils.ip_pools import fz_ip_pool
from fzutils.spider.async_always import *

class SdkCnSipder(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=fz_ip_pool,
        )
        self.max_new_page_num = 50

    async def _get_phone_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://sdk.cn/news',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    async def _get_one_page_new_info(self, page_num) -> str:
        '''
        获取单页news
        :return:
        '''
        params = (
            ('category_id', '-1'),
            ('page', str(page_num)),
        )
        url = 'https://sdk.cn/news/load-news'
        data = json_2_dict(await unblock_request(
            url=url,
            headers=await self._get_phone_headers(),
            params=params,
            ip_pool_type=self.ip_pool_type)).get('html', '')
        # pprint(data)

        return data

    async def _get_all_news(self) -> list:
        '''
        获取所有news
        :return:
        '''
        _ = []
        for base in range(1, self.max_new_page_num, self.concurrency):
            tasks = []
            for page_num in range(base, base+self.concurrency, 1):
                print('create task {}...'.format(page_num))
                tasks.append(self.loop.create_task(self._get_one_page_new_info(page_num=page_num)))
            tmp = await async_wait_tasks_finished(tasks=tasks)
            for item in tmp:
                if item != '':
                    _.append(item)

        return _

    async def _fck_run(self):
        news_list = await self._get_all_news()
        pprint(news_list)
        print('news 总个数:{}'.format(len(news_list)))

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = SdkCnSipder()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())