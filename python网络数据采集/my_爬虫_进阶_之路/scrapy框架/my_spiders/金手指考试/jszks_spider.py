# coding:utf-8

'''
@author = super_fazai
@File    : jszks_spider.py
@connect : superonesfazai@gmail.com
'''

"""
金手指考试spider
"""

from gc import collect
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class JSZKSSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool
        )
        self.concurrency = 50

    async def _fck_run(self):
        pass

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = JSZKSSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())