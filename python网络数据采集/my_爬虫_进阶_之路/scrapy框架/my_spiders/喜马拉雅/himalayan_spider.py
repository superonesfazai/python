# coding:utf-8

'''
@author = super_fazai
@File    : himalayan_spider.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class HimalayanSpider(AsyncCrawler):
    def __init__(self,):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )

    async def _fck_run(self):
        pass

if __name__ == '__main__':
    loop = get_event_loop()
    _ = HimalayanSpider()
    res = loop.run_until_complete(_._fck_run())
