# coding:utf-8

'''
@author = super_fazai
@File    : eye_check_spider.py
@connect : superonesfazai@gmail.com
'''

"""
天眼查m站
"""

from gc import collect
from asyncio import get_event_loop
from scrapy.selector import Selector
from fzutils.internet_utils import get_random_phone_ua
from fzutils.spider.fz_requests import Requests

class EyeCheckSpider(object):
    def __init__(self):
        pass

    async def _search(self, search_key) -> list:
        '''
        天眼查搜索功能
        :param search_key: 待搜索key
        :return:
        '''
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://m.tianyancha.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        params = (
            ('key', str(search_key)),
        )
        url = 'https://m.tianyancha.com/search'
        body = Requests.get_url_body(url=url, headers=headers, params=params, cookies=None)
        # print(body)
        if body == '':
            return []

        search_list = []
        try:
            # div.new-border-bottom
            search_res = Selector(text=body).css('div.search_result_container ::text').extract_first() or ''
            company_name = Selector(text=search_res).css('div.new-border-bottom a span text ::text').extract_first() or ''
            assert company_name != '', 'company_name为空值!'
            url = Selector(text=search_res).css('div.new-border-bottom a ::attr("href")').extract_first() or ''
            assert url != '', 'url为空值!'
            legal_person = Selector(text=search_res).css('a.legalPersonName ::text').extract_first() or ''
            legal_person_url = Selector(text=search_res).css('a.legalPersonName ::attr("href")').extract_first() or ''
            legal_person_url = 'https://m.tianyancha.com' + legal_person_url if legal_person_url != '' else ''

        except AssertionError as e:
            print(e)
            return []

    async def _fck_run(self):
        search_key = 'aa'
        await self._search(search_key=search_key)

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = EyeCheckSpider()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())