# coding:utf-8

'''
@author = super_fazai
@File    : eleme_spider.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

def _get_el_home_api_info():
    '''
    获取饿了吗主页接口信息
    :return:
    '''
    def _get_one(page_num):
        '''
        得到一个
        :param page_num:
        :return:
        '''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authority': 'h5.ele.me',
            'user-agent': get_random_phone_ua(),
            'accept': '*/*',
            'referer': 'https://h5.ele.me/msite/',
            # 'x-shard': 'loc=116.407173,39.90469',
        }
        cookies = {
            # SID 必须不为空
            'SID': 'p4myEPcY6MUutK3Jpxte7svwmDjYQ9lTxl2g',
            'USERID': '834460394',
            'UTUSER': '834460394',
            # 下面这些cookie参数都可为空
            # '_utrace': '',
            # 'cna': '',
            # 'isg': '',
            # 'perf_ssid': '',
            # 'track_id': '',
            # 'ubt_ssid': '',
        }
        params = (
            ('latitude', '39.90469'),
            ('longitude', '116.407173'),
            # ('offset', '0'),        # 返回的页码, 以8累加自增
            ('offset', str(page_num * 8)),
            ('limit', '8'),
            ('extras\\[\\]', ['activities', 'tags']),
            ('extra_filters', 'home'),
            # ('rank_id', 'f739de032b314314bb0d47875d46fe5f'),  # rank_id在上一个请求中, 但是测试发现可不带rang_id, 于是可以并发
            ('terminal', 'h5'),
        )
        url = 'https://h5.ele.me/restapi/shopping/v3/restaurants'
        data = json_2_dict(
            json_str=Requests.get_url_body(
                url=url,
                headers=headers,
                params=params,
                cookies=cookies,
                ip_pool_type=tri_ip_pool),
            default_res={}).get('items', [])
        # print(data)

        return data

    for page_num in range(0, 200):
        one = _get_one(page_num=page_num)
        print(one)

    return []

_get_el_home_api_info()





