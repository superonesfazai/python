# coding:utf-8

'''
@author = super_fazai
@File    : qq_music_spider.py
@connect : superonesfazai@gmail.com
'''

"""
qq音乐爬虫
"""

from gc import collect
from fzutils.spider.async_always import *

class QQMusicSpider(object):
    def __init__(self):
        self.loop = get_event_loop()
        self._t = lambda x: str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))

    async def _get_headers(self) -> dict:
        return {
            'origin': 'https://y.qq.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_phone_ua(),
            'accept': 'application/json',
            'referer': 'https://y.qq.com/m/index.html',
            'authority': 'c.y.qq.com',
        }

    async def _search_music_info(self, music_name, qq_num=1006770934) -> dict:
        '''
        搜索音乐信息
        :param music_name: 音乐名
        :return:
        '''
        params = (
            ('g_tk', '1147230719'),
            ('uin', str(qq_num)),
            ('format', 'json'),
            ('inCharset', 'utf-8'),
            ('outCharset', 'utf-8'),
            ('notice', '0'),
            ('platform', 'h5'),
            ('needNewCode', '1'),
            ('w', str(music_name)),
            ('zhidaqu', '1'),
            ('catZhida', '1'),
            ('t', '0'),
            ('flag', '1'),
            ('ie', 'utf-8'),
            ('sem', '1'),
            ('aggr', '0'),
            ('perpage', '20'),
            ('n', '20'),
            ('p', '1'),
            ('remoteplace', 'txt.mqq.all'),
            ('_', self._t),
        )
        url = 'https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp'
        data = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_headers(), params=params)).get('data', {})
        pprint(data)

        return data

    async def _get_ranking_list(self, qq_num=1006770934) -> list:
        '''
        获取qq music排行榜信息
        :return:
        '''
        params = (
            ('g_tk', '1147230719'),
            ('uin', str(qq_num)),
            ('format', 'json'),
            ('inCharset', 'utf-8'),
            ('outCharset', 'utf-8'),
            ('notice', '0'),
            ('platform', 'h5'),
            ('needNewCode', '1'),
            ('_', self._t),
        )
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_myqq_toplist.fcg'
        data = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_headers(), params=params)).get('data', {}).get('topList', [])
        # pprint(data)

        return data

    async def _fck_run(self):
        ranking_list = await self._get_ranking_list()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = QQMusicSpider()
    loop = get_event_loop()
    # res = loop.run_until_complete(_._fck_run())

    # 搜索音乐
    res = loop.run_until_complete(_._search_music_info(music_name='rich'))