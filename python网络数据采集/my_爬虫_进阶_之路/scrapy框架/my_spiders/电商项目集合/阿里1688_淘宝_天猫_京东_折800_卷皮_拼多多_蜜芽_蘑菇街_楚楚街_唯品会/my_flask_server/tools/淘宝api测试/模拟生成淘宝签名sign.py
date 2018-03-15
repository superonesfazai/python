# coding:utf-8

'''
@author = super_fazai
@File    : 模拟生成淘宝签名sign.py
@Time    : 2018/1/30 13:11
@connect : superonesfazai@gmail.com
'''

"""
jsv:2.4.8
appKey:12574478
t:1517284781823
sign:8c142bf3266484423aaa44854cab6bbd
api:mtop.ju.data.get
v:1.0
type:jsonp
dataType:jsonp
callback:mtopjsonp1
data:{"bizCode":"tejia_002","optStr":"{\"cardType\":[\"9.9\",\"39\",\"69\"],\"includeForecast\":true,\"topItemIds\":[]}"}
"""

'''
api:mtop.ju.data.get
appKey:12574478
callback:mtopjsonp1
dataType:jsonp
data:{"bizCode":"tejia_002","optStr":"{\"cardType\":[\"9.9\",\"39\",\"69\"],\"includeForecast\":true,\"topItemIds\":[]}"}
'''

'''
官方js生成sign可能在下面的功能函数中
function p(e)
'''
# js中为 sign:来查找sign
# sign = = p(o.token + "&" + a + "&" + s + "&" + n.data)

# o.token = 'ed7bbebb6bb1d';
# a = str(time.time().__round__()) + str(randint(100, 999))     # time.time().__round__() 表示保留到个位
# s = 12574478      # appKey
# n.data = this.params.data =
# "{"bizCode":"tejia_002","optStr":"{\"cardType\":[\"9.9\",\"39\",\"69\"],\"topItemIds\":[]}"}"

# tmp_1 = JSON.stringify({"bizCode":"tejia_002","optStr":"{\"cardType\":[\"9.9\",\"39\",\"69\"],\"topItemIds\":[]}"})

# e = "ed7bbebb6bb1d" + "&" + (new Date).getTime() + "&" + "12574478" + "&" + tmp_1

import time
# from time import sleep, time
from random import randint
import re, requests, json
import execjs
from pprint import pprint

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'h5api.m.taobao.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',      # 随机一个请求头
}

# 打开js源文件
with open('./get_h_func.js', 'r') as f:
    js = f.read()

js_parser = execjs.compile(js)  #  编译js得到python解析对象

t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

# 构造参数e
e = 'undefine' + '&' + t + '&' + '12574478' + '&' + '{"optStr":"{\"displayCount\":4,\"topItemIds\":[]}","bizCode":"tejia_003","currentPage":"1","pageSize":"4"}'

sign = js_parser.call('h', e)

data = json.dumps({
    'bizCode': 'tejia_004',
    'currentPage': 1,
    'optStr': json.dumps({
        'priceScope': {},
        'category': [],
        'activityId': '',
        'priceSortType': '',
        'itemLabels': ["tejia_cate_psqb"],
    }),
    'pageSize': 20,
    'salesSites': '9',
})

params = {
    "jsv": "2.4.8",
    "appKey": "12574478",
    "t": t,
    "sign": sign,
    "api": "mtop.ju.data.get",
    "v": "1.0",
    "AntiCreep": "true",
    "timeout": "5000",
    "type": "jsonp",
    "dataType": "jsonp",
    "callback": "mtopjsonp7",
    "data": data,
}

try:
    base_url = 'https://h5api.m.taobao.com/h5/mtop.ju.data.get/1.0/'
    # t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
    # print(t)

    s = requests.session()
    response = s.get(url=base_url, params=params, headers=headers)
    _m_h5_tk = response.cookies['_m_h5_tk']
    _m_h5_tk = _m_h5_tk.split('_')[0]

    print(response.text)
    # print(s.cookies.items())
    print(_m_h5_tk)

    t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
    e = _m_h5_tk + '&' + t + '&' + '12574478' + '&' + data
    # 计算正确的sign
    sign = js_parser.call('h', e)

    params['t'], params['sign'] = t, sign

    r = s.get(url=base_url, params=params, headers=headers, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
    # print(r.content.decode('utf-8'))
except:
    print('error')

body = r.content.decode('utf-8')
try:
    body = re.compile(r'\((.*?)\)').findall(body)[0]
    data = json.loads(body)
    # pprint(data)
    print(data)
except:
    print('error_2')

