# coding:utf-8

'''
@author = super_fazai
@File    : 58_spider.py
@connect : superonesfazai@gmail.com
'''

"""
test: 58 spider(其商家phone为db内部转接, 具有时效性)
"""

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

async def _get_phone_headers():
    return {
        'Host': 'yaofa.58.com',
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': get_random_phone_ua(),
        'accept-language': 'zh-cn',
    }

async def _get_one_api_list() -> list:
    '''
    获取某个city的单页信息
    :return:
    '''
    headers = await _get_phone_headers()
    headers.update({
        # 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/7.0.2(0x17000222) NetType/WIFI Language/zh_CN',
        # 'referer': 'https://servicewechat.com/wx86c7b0019914401c/66/page-frame.html',
    })
    params = (
        ('xxgl5', 'undefined'),
        ('appid', 'wx86c7b0019914401c'),
        ('userid', ''),
        ('releaseId', ''),
        ('mpId', ''),
        ('env58', 'true'),
        ('test', ''),
        ('page', '1'),
        ('size', '20'),
        ('city', '杭州'),
        ('sort', 'visit_desc'),
        ('latitude', '30.192995071411133'),
        ('longitude', '120.19691467285156'),
    )
    url = 'https://yaofa.58.com/search/mapp'
    data = json_2_dict(
        json_str=Requests.get_url_body(url=url, headers=headers, params=params, ip_pool_type=tri_ip_pool),
        default_res={}).get('data', [])
    pprint(data)

    return data

async def _get_one_card_list() -> list:
    '''
    商家单页card list
    :return:
    '''
    # 商家卡片
    headers = await _get_phone_headers()
    headers.update({
        # 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/7.0.2(0x17000222) NetType/WIFI Language/zh_CN',
        # 'referer': 'https://servicewechat.com/wx86c7b0019914401c/66/page-frame.html',
    })
    params = (
        ('yhlsn', 'undefined'),
        ('appid', 'wx86c7b0019914401c'),
        ('userid', ''),
        ('releaseId', ''),
        ('mpId', ''),
        ('env58', 'true'),
        ('test', ''),
        ('latitude', '30.19283676147461'),
        ('longitude', '120.19671630859375'),
    )
    url = 'https://yaofa.58.com/search/card'
    data = json_2_dict(
        json_str=Requests.get_url_body(url=url, headers=headers, params=params, ip_pool_type=tri_ip_pool),
        default_res={}).get('data', [])
    pprint(data)

    return data

async def _get_one_company_info():
    '''
    单个商家详情
    :return:
    '''
    headers = await _get_phone_headers()
    headers.update({
        # 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/7.0.2(0x17000222) NetType/WIFI Language/zh_CN',
        # 'referer': 'https://servicewechat.com/wx86c7b0019914401c/66/page-frame.html',
    })
    params = (
        ('yhucg', 'undefined'),
        ('appid', 'wx86c7b0019914401c'),
        ('userid', ''),
        ('releaseId', '1067334831769436160'),
        ('mpId', ''),
        ('env58', 'true'),
        ('test', ''),
        ('userId', '30731492679942'),
        ('appId', 'yxxdOD0CxOpgVpz5t'),
        ('consumerId', '1085454992565657600'),
    )
    url = 'https://yaofa.58.com/search/detail'
    data = json_2_dict(
        json_str=Requests.get_url_body(url=url, headers=headers, params=params, ip_pool_type=tri_ip_pool),
        default_res={}).get('data', {})
    pprint(data)

    return data

async def _get_phone() -> str:
    '''
    手机号(测试发现电话号码是变化的, 具有时效性)
    :return:
    '''
    headers = await _get_phone_headers()
    headers.update({
        # 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/7.0.2(0x17000222) NetType/WIFI Language/zh_CN',
        # 'referer': 'https://servicewechat.com/wx86c7b0019914401c/66/page-frame.html',
    })
    params = (
        ('ziswi', 'undefined'),
        ('appid', 'yxxdOD0CxOpgVpz5t'),
        ('userid', '30731492679942'),
        ('releaseId', '1068093878445588480'),
        ('mpId', '1067334831769436160'),
        ('env58', 'true'),
        ('test', ''),
        ('from', 'index'),
        ('sign', ''),
        ('cardid',
         dumps({
             '_relatedInfo': {
                 'anchorRelatedText': '\n'
                                       '卓永彪好吃的面饭\n'
                                       '58合作商家\n'
                                       '公司地址： 杭州市拱墅区万达广场商业街1－107号\n'
                                       '联系电话： 点击获取电话号码\n',
                  'anchorTapTime': 1547630972294,
                  'anchorTargetText': '点击获取电话号码'},
            '_requireActive': True,
            'changedTouches': [{
                'clientX': 157,
                'clientY': 153,
                'force': 0,
                'identifier': 1906136134,
                'pageX': 157,
                'pageY': 153
            }],
            'currentTarget': {
                'dataset': {'tel': '-'},
                'id': '',
                'offsetLeft': 16,
                'offsetTop': 137
            },
            'detail': {
                'x': 157,
                'y': 153
            },
            'target': {
                'dataset': {},
                'id': '',
                'offsetLeft': 91,
                'offsetTop': 11
            },
            'timeStamp': 84601,
            'touches': [{
                'clientX': 157,
                'clientY': 153,
                'force': 0,
                'identifier': 1906136134,
                'pageX': 157,
                'pageY': 153
            }],
            'type': 'tap'
         }))
    )
    data = json_2_dict(
        json_str=Requests.get_url_body('https://yaofa.58.com/other/encrypt/phone', headers=headers, params=params, ip_pool_type=tri_ip_pool),
        default_res={}).get('data', '')
    print(data)

    return data

loop = get_event_loop()
# res = loop.run_until_complete(_get_one_api_list())
# res = loop.run_until_complete(_get_one_card_list())
# res = loop.run_until_complete(_get_one_company_info())
res = loop.run_until_complete(_get_phone())
