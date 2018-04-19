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
    'cookie': 'ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiI5WmZucV96VDl6NDhTOTg4WkNsaFpxSEwiLCJfZXhwaXJlIjoxNTI0MTE5MzI3NDQ5LCJfbWF4QWdlIjo4NjQwMDAwMH0=; ',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://m.1688.com/page/offerRemark.htm?offerId=42735065607',
    'x-requested-with': 'XMLHttpRequest',
}

goods_id = '42735065607'
data = json.dumps({
    'data': {
        'offerId': goods_id,
        # 'receiveUserId': 2318703732,
        'starLevel': 7,
        'itemId': int(goods_id),
        'bizType': 'trade',
        'page': 1,
        'pageSize': 5,
    }
})

params = (
    # ('_csrf', 'xMrEnTz7-VByOlidz0AzkXFg_ifMZBv6bCA0'),
    ('_csrf', ''),
    ('__wing_navigate_type', 'view'),
    ('__wing_navigate_url', 'detail:modules/offerRemarkList/view'),
    # ('__wing_navigate_options', '{"data":{"offerId":"42735065607","receiveUserId":2318703732,"starLevel":7,"itemId":42735065607,"bizType":"trade","page":1,"pageSize":5}}'),
    ('__wing_navigate_options', data),
    ('_', '1524101787703'),
)

s = requests.session()
_url = 'https://m.1688.com/page/offerRemark.htm'
# response = s.get(_url, headers=headers, params=params)
# print(response.content.decode('utf-8'))
body = MyRequests.get_url_body(url=_url, headers=headers, params=params)
# print(body)

try:
    _ = json.loads(body).get('data', {}).get('model', [])
    pprint(_)
except Exception as e:
    print('json转换body时出错, 请检查!')
    _ = []

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://m.1688.com/page/offerRemark.htm?_csrf=xMrEnTz7-VByOlidz0AzkXFg_ifMZBv6bCA0&__wing_navigate_type=view&__wing_navigate_url=detail%3Amodules%2FofferRemarkList%2Fview&__wing_navigate_options=%7B%22data%22%3A%7B%22offerId%22%3A%2242735065607%22%2C%22receiveUserId%22%3A2318703732%2C%22starLevel%22%3A7%2C%22itemId%22%3A42735065607%2C%22bizType%22%3A%22trade%22%2C%22page%22%3A1%2C%22pageSize%22%3A5%7D%7D&_=1524101787703', headers=headers)
