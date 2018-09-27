# coding:utf-8

'''
@author = super_fazai
@File    : china_adjue_docs_spider.py
@connect : superonesfazai@gmail.com
'''

from asyncio import get_event_loop
from gc import collect

class ChinaAdjueDocsSpider(object):
    def __init__(self):
        self.loop = get_event_loop()

    async def _fck_run(self):
        '''
        main
        :return:
        '''


    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = ChinaAdjueDocsSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())