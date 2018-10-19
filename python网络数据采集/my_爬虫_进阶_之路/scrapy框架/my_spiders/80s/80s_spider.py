# coding:utf-8

'''
@author = super_fazai
@File    : 80s_spider.py
@connect : superonesfazai@gmail.com
'''

"""
80s电影网spider
"""

from gc import collect
from fzutils.spider.async_always import *

class _80sSpider(object):
    def __init__(self):
        self.keyword = ''
        self.loop = get_event_loop()

    async def _get_headers(self):
        return {
            'authority': 'm.80s.tw',
            'cache-control': 'max-age=0',
            'origin': 'https://m.80s.tw',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://m.80s.tw/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    async def _search(self) -> list:
        '''
        搜索电影
        :return:
        '''
        data = {
            'keyword': str(self.keyword),
        }
        url = 'https://m.80s.tw/search'
        body = Requests.get_url_body(method='post', url=url, headers=await self._get_headers(), data=data)
        # print(body)

        films_info_list = Selector(text=body).css('div.list-group a').extract() or []
        # pprint(films_info_list)
        films_list = []
        for item in films_info_list:
            try:
                score = Selector(text=item).css('span ::text').extract_first() or ''
                url = Selector(text=item).css(' ::attr("href")').extract_first() or ''
                assert url != '', '获取到的url为空值!'
                url = 'https://www.80s.tw' + url
                year = int(Selector(text=item).css('h4 small ::text').extract_first() or '')
                title = re.compile('</span>(.*?)<small>').findall(item)[0]
                title = title.replace(' ', '')
                assert title != '', 'title为空值!'
                sub_title = Selector(text=item).css('p ::text').extract_first() or ''
                assert sub_title != '', 'sub_title为空值!'
            except (AssertionError, ValueError, IndexError) as e:
                print(e)
                continue
            films_list.append({
                'title': title,             # 电影名
                'score': score,             # 分数
                'url': url,                 # 地址
                'year': year,               # 出版年限
                'sub_title': sub_title,     # 子标题
            })

        return films_list

    async def _fck_run(self, keyword):
        self.keyword = keyword
        films_list = await self._search()
        pprint(films_list)

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = _80sSpider()
    keyword = '我不是药神'
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run(keyword=keyword))
