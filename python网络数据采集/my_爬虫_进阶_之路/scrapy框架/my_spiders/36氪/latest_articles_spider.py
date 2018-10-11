# coding:utf-8

'''
@author = super_fazai
@File    : latest_articles_spider.py
@connect : superonesfazai@gmail.com
'''

"""
36氪最新文章spider
"""

from gc import collect
from time import sleep
from pprint import pprint
from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua
from fzutils.common_utils import (
    json_2_dict,
    get_random_int_number,)
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,)

class _36Krypton(object):
    def __init__(self):
        pass

    def _get_one_page_articles(self, page_num) -> list:
        '''
        得到一页新闻
        :param page_num:
        :return:
        '''
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Accept': '*/*',
            'Referer': 'https://36kr.com/',
            'Connection': 'keep-alive',
        }

        params = (
            ('per_page', '20'),
            ('page', str(page_num)),
            ('_', str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))),
        )

        url = 'https://36kr.com/api/search-column/mainsite'
        data = json_2_dict(Requests.get_url_body(url=url, headers=headers, params=params, cookies=None)).get('data', {}).get('items', [])
        # pprint(data)
        if data == []:
            return []

        [item.update({
            'user_info': json_2_dict(item.get('user_info', ''))
        }) for item in data]
        # pprint(data)

        return data

    def _crawl_all_lastest_articles(self):
        '''
        抓取所有最新文章
        :return:
        '''
        all = []
        for page_num in range(1, 3100):
            one_res = self._get_one_page_articles(page_num=page_num)
            # print(one_res)
            all += one_res

            label = '+' if one_res != [] else '-'
            print('[{}] 第{}页...'.format(label, page_num))

        return all

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = _36Krypton()
    _._crawl_all_lastest_articles()
