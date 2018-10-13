# coding:utf-8

'''
@author = super_fazai
@File    : wy_news_spider.py
@connect : superonesfazai@gmail.com
'''

"""
网易新闻爬虫
"""

from gc import collect
from fzutils.spider.async_always import *

class WYNewsSpider(object):
    def __init__(self):
        self.loop = get_event_loop()

    async def _get_phone_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Accept': '*/*',
            # 'Referer': 'https://3g.163.com/touch/news/',
            'Connection': 'keep-alive',
        }

    async def _get_one_page_info(self, start_page_num) -> list:
        '''
        获取一页信息
        :return:
        '''
        url = 'https://3g.163.com/touch/reconstruct/article/list/BBM54PGAwangning/{}-10.html'.format(start_page_num)
        body = Requests.get_url_body(url=url, headers=await self._get_phone_headers(), cookies=None)
        # print(body)
        if body == '':
            print('获取到的body为空值!')
            return []

        try:
            data = json_2_dict(re.compile('\((.*)\)').findall(body)[0])
        except IndexError:
            print('获取data时索引异常!')
            data = {}

        return data.get('BBM54PGAwangning', [])

    async def _fck_run(self):
        start_page_num_list = list(range(0, 310, 10))   # 300以后就是没有更多新闻了.
        tasks = []
        for start_page_num in start_page_num_list:
            print('创建task: {}'.format(start_page_num))
            tasks.append(self.loop.create_task(self._get_one_page_info(start_page_num=start_page_num)))

        all_tasks_res = await async_wait_tasks_finished(tasks=tasks)
        all_page_list = []
        for item in all_tasks_res:
            all_page_list += item

        pprint(all_page_list)
        print('总共采集新闻数:{}'.format(len(all_page_list)))

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = WYNewsSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())