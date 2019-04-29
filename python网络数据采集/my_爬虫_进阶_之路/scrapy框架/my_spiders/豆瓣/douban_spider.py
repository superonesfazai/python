# coding:utf-8

'''
@author = super_fazai
@File    : douban_spider.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class DouBanSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool
        )

    async def _fck_run(self):
        tasks = []
        for page_num in range(0, 100):
            print('create task[where page_num: {}]'.format(page_num))
            tasks.append(self.loop.create_task(self._get_home_page_recommend_one_api_info(
                page_num=page_num,
            )))

        one_res = await async_wait_tasks_finished(tasks=tasks)
        # pprint(one_res)

        res = []
        for i in one_res:
            for j in i:
                res.append(j)
        pprint(res)
        print('res.len: {}'.format(len(res)))

    async def _get_home_page_recommend_one_api_info(self, page_num:int) -> list:
        """
        获取首页推荐的单页信息
        :return:
        """
        headers = await self._get_phone_headers()
        headers.update({
            'Referer': 'https://m.douban.com/',
        })
        params = (
            ('start', str(page_num)),
            ('count', '20'),
            ('loc_id', '108288'),
            ('gender', ''),
            ('birthday', ''),
            # ('udid', '9fcefbf2acf1dfc991054ac40ca5114be7cd092f'),
            ('for_mobile', '1'),
        )
        body = await unblock_request(
            url='https://m.douban.com/rexxar/api/v2/elendil/recommend_feed',
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=8,)
        data = json_2_dict(
            json_str=body,).get('items', [])
        # pprint(data)

        print('[{}] page_num: {}'.format(
            '+' if data != [] else '-',
            page_num,
        ))

        return data

    async def _get_phone_headers(self):
        return {
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': get_random_phone_ua(),
        }

if __name__ == '__main__':
    loop = get_event_loop()
    _ = DouBanSpider()
    res = loop.run_until_complete(_._fck_run())