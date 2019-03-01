# coding:utf-8

'''
@author = super_fazai
@File    : youyuan_spider.py
@connect : superonesfazai@gmail.com
'''

"""
有缘网spider
"""

from gc import collect
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.selector import async_parse_field
from fzutils.spider.async_always import *

class YouYuanSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=tri_ip_pool,
        )

    async def _fck_run(self):
        pass

    async def _get_conditional_search_one_page_info(self, page_num, age_start=20, age_end=25) -> dict:
        """
        得到条件搜索中单页的信息
        :param page_num:
        :return:
        """
        url = 'http://www.youyuan.com/find/hangzhou/mm{age_start}-{age_end}/advance-0-0-0-0-0-0-0/p{page_num}/'.format(
            age_start=age_start,
            age_end=age_end,
            page_num=page_num,
        )
        body = Requests.get_url_body(
            url=url,
            headers=await self._get_pc_headers(),
            cookies=None,
            ip_pool_type=self.ip_pool_type,
            num_retries=6)
        # print(body)

        li_item_selector = {
            'method': 'css',
            'selector': 'li.search_user_item',
        }
        li_item = await async_parse_field(
            parser=li_item_selector,
            target_obj=body,
            is_first=False,)
        for li in li_item:
            print(li)

        return {}

    async def _get_pc_headers(self):
        return {
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def __del__(self):
        pass

if __name__ == '__main__':
    _ = YouYuanSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())