# coding:utf-8

'''
@author = super_fazai
@File    : whatismybrowser_spider.py
@connect : superonesfazai@gmail.com
'''

"""
whatismybrowser user-agent spider
"""

from gc import collect
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.selector import async_parse_field
from fzutils.spider.async_always import *

class UASpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
            *params,
            **kwargs,
        )
        self.concurrency = 10

    async def _fck_run(self):
        await self._get_all_ua_list()

    async def _get_all_ua_list(self) -> list:
        '''
        获取所有ua
        :return:
        '''
        tasks = []
        for page_num in range(1, 12):
            print('create task[where page_num:{}]...'.format(page_num))
            tasks.append(self.loop.create_task(self._get_one_page_ua_list(page_num=page_num)))

        one_res = await async_wait_tasks_finished(tasks=tasks)
        all_ua_list = []
        for i in one_res:
            for j in i:
                if j not in all_ua_list:
                    all_ua_list.append(j)

        pprint(all_ua_list)
        print('all ua len: {}'.format(len(all_ua_list)))

        return all_ua_list

    async def _get_one_page_ua_list(self, page_num) -> list:
        '''
        获取单页的ua list
        :return:
        '''
        url = 'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/{}'.format(page_num)
        body = await unblock_request(
            url=url,
            headers=await self._get_phone_headers(),
            ip_pool_type=self.ip_pool_type)
        # print(body)

        ua_selector = {
            'method': 'css',
            'selector': 'td.useragent a ::text',
        }
        ua_list = await async_parse_field(parser=ua_selector, target_obj=body, is_first=False)
        # pprint(ua_list)

        print('[{}] page_num: {}'.format('+' if ua_list != [] else '-', page_num))

        return ua_list

    async def _get_phone_headers(self):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'If-Modified-Since': 'Sat, 26 Jan 2019 21:19:54 GMT',
        }

    async def _get_pc_headers(self):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = UASpider()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())
