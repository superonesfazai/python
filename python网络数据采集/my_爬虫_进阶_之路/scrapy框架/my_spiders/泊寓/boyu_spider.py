# coding:utf-8

'''
@author = super_fazai
@File    : boyu_spider.py
@connect : superonesfazai@gmail.com
'''

"""
泊寓爬虫
"""

from gc import collect
from logging import getLogger
from fzutils.spider.async_always import *

class BoYuSpider(object):
    def __init__(self):
        self.loop = get_event_loop()
        self._set_city_uuid_dict()

    def _set_city_uuid_dict(self):
        self.city_uuid_dict = {
            '北京': '1734a7ef-3140-11e6-8744-00163e003632',
            '长春': '5922ad7a-decd-11e6-9611-1051721bd1ff',
            '长沙': '593f021b-3140-11e6-8744-00163e003632',
            '重庆': 'edf69c30-6ea0-11e6-a9e7-00163e003632',
            '大连': '63c00d91-78c9-11e7-8d67-1051721bd1ff',
            '东莞': 'bc9f3a1f-0658-11e6-8426-d89d672b932c',
            '福州': '6e1b75bd-3140-11e6-8744-00163e003632',
            '佛山': '7fb2f119-3140-11e6-8744-00163e003632',
            '广东': 'd10eb7a0-313f-11e6-8744-00163e003632',
            '合肥': '22bfe544-3140-11e6-8744-00163e003632',
            '杭州': 'cb10954a-6e9e-11e6-a9e7-00163e003632',
            '济南': '6443c97a-3140-11e6-8744-00163e003632',
            '南京': '08e7a536-78c8-11e7-8d67-1051721bd1ff',
            '南通': '129870e6-7da4-11e7-8d67-1051721bd1ff',
            '宁波': 'b94e9c3a-54b4-11e7-9611-1051721bd1ff',
            '青岛': '36e9800c-45f1-11e7-9611-1051721bd1ff',
            '苏州': '25d88af1-8162-11e7-8d67-1051721bd1ff',
            '沈阳': '8d048cae-3140-11e6-8744-00163e003632',
            '深圳': 'c282c843-c3fd-11e5-9267-00163e003632',
            '上海': 'ff7ce3d4-313f-11e6-8744-00163e003632',
            '天街': '5d2d8c60-78c9-11e7-8d67-1051721bd1ff',
            '武汉': '74ed3be7-6ea0-11e6-a9e7-00163e003632',
            '芜湖': '9f2306be-236a-11e8-96eb-00163e0c8af1',
            '乌鲁木齐': 'c1700dc2-3439-11e6-8744-00163e003632',
            '厦门': '99ee380d-3140-11e6-8744-00163e003632',
            '西安': 'ad969e39-3439-11e6-8744-00163e003632',
            '徐州': 'cfd0b1f3-4a65-11e7-9611-1051721bd1ff',
            '郑州': 'f8f2bd15-fe7b-11e6-9611-1051721bd1ff',
        }

    async def _get_city_uuid(self, city_name) -> str:
        '''
        得到对应城市的uuid
        :param city_name:
        :return:
        '''
        city_uuid = ''
        for key, value in self.city_uuid_dict.items():
            if city_name in key:
                city_uuid = value
                break

        return city_uuid

    async def _get_pc_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Accept': '*/*',
            # 'Referer': 'https://www.inboyu.com/house-type/list?area=%E8%A5%BF%E6%B9%96%E5%8C%BA',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    async def _search_house_resources(self, city_name):
        '''
        搜索房源
        :return:
        '''
        city_uuid = await self._get_city_uuid(city_name)
        assert city_uuid != '', 'city_name不存在!'

        cookies = {
            'cityId': 'cb10954a-6e9e-11e6-a9e7-00163e003632',
        }
        url = 'https://www.inboyu.com/project/get-list-data'
        data = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_pc_headers(), cookies=cookies))
        # pprint(data)

        return data

    async def _fck_run(self):
        await self._search_house_resources(city_name='杭州')

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = BoYuSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())