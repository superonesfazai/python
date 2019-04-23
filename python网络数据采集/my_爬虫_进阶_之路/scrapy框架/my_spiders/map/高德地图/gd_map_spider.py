# coding:utf-8

'''
@author = super_fazai
@File    : gd_map_spider.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
from fzutils.internet_utils import get_random_phone_ua
from fzutils.spider.fz_requests import Requests
from fzutils.ip_pools import tri_ip_pool
from fzutils.common_utils import json_2_dict

# 高德map 单页shop搜索
headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'user-agent': get_random_phone_ua(),
    'accept': 'application/json',
    'referer': 'https://m.amap.com/search/view/keywords=%E8%A1%A3%E6%9C%8D',
    'authority': 'm.amap.com',
    'x-requested-with': 'XMLHttpRequest',
}

params = (
    ('pagenum', '2'),
    ('user_loc', '120.153576,30.287459'),
    ('geoobj', '120.089203|30.177242|120.217949|30.397676'),
    ('city', '杭州'),
    ('keywords', '衣服'),
    ('cluster_state', '5'),
    ('client_network_class', '4'),
    # ('uuid', '2a21e0af-009d-4a1a-a63e-ee5c6dec2488'),
    # ('smToken', 'token'),
    # ('smSign', 'undefined'),
)
# 以下参数必传
cookies = {
    # 'UM_distinctid': '',
    # 'cna': '',
    # 'dev_help': '',
    'guid': '0ea8-fd21-faea-32f9',
    # 'isg': '',
    'key': 'bfe31f4e0fb231d29e1d3ce951e2c780',
    # 'l': '',
    # 'passport_login': '',
    # 'sc_is_visitor_unique': '',
    'x5sec': '7b22617365727665723b32223a223666613532376137326239333766343233636561326462613466633364653861434c2f762b655546454b726772496a66736376653867453d227d',
}
url = 'https://m.amap.com/service/poi/keywords.json'
body = Requests.get_url_body(
    url=url,
    headers=headers,
    params=params,
    cookies=cookies,
    ip_pool_type=tri_ip_pool,)
# print(body)
data = json_2_dict(
    json_str=body,).get('poi_list', [])
pprint(data)