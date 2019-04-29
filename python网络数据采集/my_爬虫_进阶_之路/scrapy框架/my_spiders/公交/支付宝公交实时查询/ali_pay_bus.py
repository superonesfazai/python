# coding:utf-8

'''
@author = super_fazai
@File    : ali_pay_bus.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

def get_ali_pay_real_time_bus_info(city_id:str,
                                   user_lng:float,
                                   user_lat:float,
                                   route_id:int,
                                   stop_id:int,):
    """
    获取ali pay某城市某巴士的实时信息
    :param city_id:
    :param user_lng:
    :param user_lat:
    :param route_id:
    :param stop_id:
    :return:
    """
    # 必传参数, 否则跳转ali_pay登录
    cookies = {
        # 'UM_distinctid': '',
        # 'CNZZDATA1272897274': '',
        'SESSION': 'a516e0fc-d1b0-482c-8f65-0ee6b208af2f',
    }
    headers = {
        'Host': 'm.ibuscloud.com',
        'Origin': 'https://cityh5.ibuscloud.com',
        'Accept': 'application/json, text/plain, */*',
        # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f NebulaSDK/1.8.100112 Nebula WK PSDType(1) AlipayDefined(nt:4G,ws:414|672|3.0) AliApp(AP/10.1.60.6001) AlipayClient/10.1.60.6001 Language/zh-Hans',
        'User-Agent': get_random_phone_ua(),
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        # 'Referer': 'https://cityh5.ibuscloud.com/',
    }
    params = (
        ('routeId', str(route_id)),
        ('stopId', str(stop_id)),
        ('userLat', str(user_lat)),
        ('userLng', str(user_lng)),
        ('city', city_id),
    )
    body = Requests.get_url_body(
        url='https://m.ibuscloud.com/v1/bus/getNextBusByRouteStopId',
        headers=headers,
        params=params,
        cookies=cookies,
        ip_pool_type=tri_ip_pool,)
    # print(body)
    data = json_2_dict(
        json_str=body,
    )
    # pprint(data)

    return data

data = get_ali_pay_real_time_bus_info(
    city_id='330100',
    user_lng=121.101452,
    user_lat=31.290417,
    route_id=1001000284,
    stop_id=1001001531,)
pprint(data)