# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2018/4/9 17:04
@connect : superonesfazai@gmail.com
'''
import sys, json, re
sys.path.append('..')
from pprint import pprint

from my_requests import MyRequests
from my_phantomjs import MyPhantomjs
from my_utils import _get_url_contain_params

import requests

headers = {
    'cookie': 'visitkey=50916190274597112; mobilev=html5; sid=394f3c80838a7161809dc760a402e451;',
    'origin': 'https://item.m.jd.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json',
    'referer': 'https://item.m.jd.com/ware/view.action?wareId=5025518',
    'authority': 'item.m.jd.com',
    'x-requested-with': 'XMLHttpRequest',
}

data = [
  ('wareId', '5025518'),
  ('offset', '1'),
  ('num', '10'),
  ('checkParam', 'LUIPPTP'),
  ('category', '670_671_1105'),
  ('isUseMobile', 'true'),
  ('evokeType', ''),
  ('type', '0'),
  ('isCurrentSku', 'false'),
]

base_url = 'https://item.m.jd.com/newComments/newCommentsDetail.json'

my_phantomjs = MyPhantomjs()
cookies = my_phantomjs.get_url_cookies_from_phantomjs_session(url='https://item.m.jd.com/')
# print(cookies)

del my_phantomjs
headers.update({'cookie': cookies})
body = MyRequests.get_url_body(url=base_url, headers=headers, params=data)
print(body)