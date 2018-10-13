# coding:utf-8

'''
@author = super_fazai
@File    : wx_public_num_spider.py
@connect : superonesfazai@gmail.com
'''

"""
获取某微信公众号所有文章地址
"""

import requests
import random
from gc import collect

from fzutils.spider.async_always import *

class WXPublicNumSpider(object):
    def __init__(self, gz_list: list):
        self.gz_list = gz_list

    async def _get_headers(self):
        return {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": get_random_pc_ua(),
        }

    async def _get_wx_public_num_cookies(self) -> dict:
        '''
        获取wx公众号的cookies
        :return:
        '''
        with open('./cookie.txt', 'r', encoding='utf-8') as f:
            cookie = f.read()
        cookies = str_cookies_2_dict(cookie)
        # pprint(cookies)

        return cookies

    async def _get_token(self) -> str:
        url = 'https://mp.weixin.qq.com'
        response = requests.get(url=url, cookies=self.cookies)
        token = re.findall(r'token=(\d+)', str(response.url))[0]
        print(token)

        return token

    async def _get_this_wx_public_num_info(self):
        '''
        获取该公众号的基本信息
        :return:
        '''
        for query in self.gz_list:
            query_id = {
                'action': 'search_biz',
                'token': self.token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'query': query,
                'begin': '0',
                'count': '5',
            }
            search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
            search_data = json_2_dict(Requests.get_url_body(url=search_url, headers=self.headers, params=query_id, cookies=self.cookies))
            lists = search_data.get('list', [])[0]
            print(lists)

            fakeid = lists.get('fakeid')
            query_id_data = {
                'token': self.token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '0',
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            appmsg_data = json_2_dict(Requests.get_url_body(url=appmsg_url, headers=self.headers, params=query_id_data, cookies=self.cookies))
            max_num = appmsg_data.get('app_msg_cnt')  # 发布的文章总数
            article_lists = appmsg_data.get('app_msg_list')  # 发布的文章lists
            pprint(article_lists)

            # 进行提取文章的代码
            num = int(int(max_num) / 5)
            begin = 0
            while num + 1 > 0:
                query_id_data.update({
                    'begin': str(begin),
                })
                print('翻页###################', begin)
                query_fakeid_response = Requests.get_url_body(url=appmsg_url, cookies=self.cookies,
                                                              headers=self.headers, params=query_id_data)
                _ = json_2_dict(query_fakeid_response)
                fakeid_list = _.get('app_msg_list')
                for item in fakeid_list:
                    print(item.get('link'))
                num -= 1
                begin = int(begin)
                begin += 5
                sleep(2)

    async def _fck_run(self):
        self.cookies = await self._get_wx_public_num_cookies()
        self.token = await self._get_token()
        self.headers = await self._get_headers()
        await self._get_this_wx_public_num_info()

    def __del__(self):
        collect()


if __name__ == '__main__':
    # 公众号的id
    gz_list = [
        'henizaiyiqisjz',
    ]
    _ = WXPublicNumSpider(gz_list=gz_list)
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())