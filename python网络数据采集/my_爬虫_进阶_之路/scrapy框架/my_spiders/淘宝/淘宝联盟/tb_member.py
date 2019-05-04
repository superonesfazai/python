# coding:utf-8

'''
@author = super_fazai
@File    : tb_member.py
@connect : superonesfazai@gmail.com
'''

"""
淘宝联盟
"""

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

goods_id = '592726369063'
# https://pub.alimama.com/promo/search/index.htm (基于tb联盟的推广链接搜索)
headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'user-agent': get_random_pc_ua(),
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'authority': 'pub.alimama.com',
    'x-requested-with': 'XMLHttpRequest',
}
# 必传参数, 标识自己的tb
cookies = {
    # '402860134_yxjh-filter-1': '',
    # 'JSESSIONID': '',
    # '_m_h5_c': '',
    # '_m_h5_tk': '',
    # '_tb_token_': '',
    # 'account-path-guide-s1': '',
    # 'alimamapw': '',
    # 'alimamapwag': '',
    # 'apushe137263758a79cda89ab56b51e15531e': '',
    # 'cna': '',
    'cookie2': '1061bfebacc257bc0c41125af568f1aa',
    # 'cookie31': '',
    # 'cookie32': '',
    # 'isg': '',
    # 'l': '',
    # 'login': '',
    # 'rurl': '',
    # 't': '',
    # 'taokeisb2c': '',
    # 'v': '',
}
params = (
    ('tag', '29'),
    ('itemId', str(goods_id)),
    ('blockId', ''),
    ('t', get_now_13_bit_timestamp()),
    # ('_tb_token_', ''),
    # ('pvid', '10_113.215.177.173_9740_1556963444009'),
)
# 获取auctionid, adzoneid
body = Requests.get_url_body(
    url='https://pub.alimama.com/common/adzone/newSelfAdzone2.json',
    headers=headers,
    params=params,
    # cookies=cookies,
    ip_pool_type=tri_ip_pool,)
# print(body)
data = json_2_dict(
    json_str=body,).get('data', {}).get('otherAdzones', [])
# pprint(data)

site_id = data[0].get('id', '')
adzone_id = data[0].get('sub', [])[0].get('id', '')
# print(site_id, adzone_id)
params = (
    ('auctionid', str(goods_id)),
    ('adzoneid', str(adzone_id)),
    ('siteid', str(site_id)),
    ('scenes', '1'),
    ('tkFinalCampaign', '20'),
    ('t', get_now_13_bit_timestamp()),
    # ('_tb_token_', ''),
    # ('pvid', ''),
)
body = Requests.get_url_body(
    url='https://pub.alimama.com/common/code/getAuctionCode.json',
    headers=headers,
    params=params,
    cookies=cookies,
    ip_pool_type=tri_ip_pool,)
# print(body)
data = json_2_dict(
    json_str=body,).get('data', {})
pprint(data)