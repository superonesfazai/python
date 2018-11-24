# coding:utf-8

'''
@author = super_fazai
@File    : ziroom_spider.py
@connect : superonesfazai@gmail.com
'''

"""
自如房源爬虫
"""

from gc import collect
from fzutils.ip_pools import fz_ip_pool
from fzutils.spider.async_always import *

class ZiRoomSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=fz_ip_pool,
        )
        self.concurrency = 10

    async def _get_phone_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Accept': '*/*',
            # 'Referer': 'http://m.ziroom.com/BJ/search?show=%E6%95%B4%E7%A7%9F&list=2&type=10',
            'Connection': 'keep-alive',
        }

    async def _get_room_filter_data(self) -> dict:
        '''
        得到房屋过滤参数
        :return:
        '''
        params = (
            ('city_code', '110000'),
        )
        url = 'http://m.ziroom.com/v7/room/filter.json'
        body = Requests.get_url_body(
            url=url,
            headers=await self._get_phone_headers(),
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=6)
        # print(body)
        data = json_2_dict(
            json_str=body,
            default_res={})

        return data

    async def _fck_run(self):
        room_filter_data = await self._get_room_filter_data()
        pprint(room_filter_data)

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = ZiRoomSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())