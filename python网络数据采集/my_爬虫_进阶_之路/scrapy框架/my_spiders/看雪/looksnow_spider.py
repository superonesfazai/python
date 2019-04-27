# coding:utf-8

'''
@author = super_fazai
@File    : looksnow_spider.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class LookSnowSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )
        self.home_page_max_page_num = 100

    async def _fck_run(self):
        tasks = []
        for page_num in range(self.home_page_max_page_num):
            print('create task[where page_num: {}]...'.format(page_num))
            tasks.append(self.loop.create_task(self._get_home_page_article_one_api_info(
                page_num=page_num
            )))

        one_res = await async_wait_tasks_finished(tasks=tasks)

        res = []
        for item in one_res:
            for j in item:
                res.append({
                    'article_name': j.get('subject'),
                })

        pprint(res)

    async def _get_home_page_article_one_api_info(self, page_num:int) -> list:
        """
        得到首页文章单页信息
        :return:
        """
        headers = await self._get_random_phone_headers()
        headers.update({
            'Origin': 'https://www.kanxue.com',
            'Referer': 'https://www.kanxue.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        })
        data = {
            'page': str(page_num),
            'pagesize': '10'
        }
        url = 'https://www.kanxue.com/homepost-morearticle.htm'
        body = await unblock_request(
            method='post',
            url=url,
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,)
        # print(body)
        data = json_2_dict(
            json_str=body).get('message', {}).get('list', [])
        # pprint(data)

        print('[{}] page_num: {}'.format(
            '+' if data != [] else '-',
            page_num,
        ))

        return data

    @staticmethod
    async def _get_random_phone_headers():
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/plain, */*; q=0.01',
            'Connection': 'keep-alive',
        }

if __name__ == '__main__':
    loop = get_event_loop()
    _ = LookSnowSpider()
    loop.run_until_complete(_._fck_run())