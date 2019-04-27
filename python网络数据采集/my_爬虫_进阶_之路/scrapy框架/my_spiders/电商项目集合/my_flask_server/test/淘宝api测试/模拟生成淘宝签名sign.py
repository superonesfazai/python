# coding:utf-8

'''
@author = super_fazai
@File    : 模拟生成淘宝签名sign.py
@Time    : 2018/1/30 13:11
@connect : superonesfazai@gmail.com
'''

"""
sign签名在于先不带sign中_m_h5_tk计算得到sign预请求一次得到cookies中的_m_h5_tk,
然后通过研究js源码根据_m_h5_tk算出sign, 再带上sign请求就得到需求数据了
"""

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

def calculate_right_sign(_m_h5_tk:str, data:json):
    '''
    根据给的json对象 data 和 _m_h5_tk计算出正确的sign
    :param _m_h5_tk:
    :param data:
    :return: sign 类型str, t 类型str
    '''
    with open('./get_h_func.js', 'r') as f:     # 打开js源文件
        js = f.read()

    js_parser = execjs.compile(js)  # 编译js得到python解析对象
    t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

    # 构造参数e
    appKey = '12574478'
    # e = 'undefine' + '&' + t + '&' + appKey + '&' + '{"optStr":"{\"displayCount\":4,\"topItemIds\":[]}","bizCode":"tejia_003","currentPage":"1","pageSize":"4"}'
    e = _m_h5_tk + '&' + t + '&' + appKey + '&' + data

    sign = js_parser.call('h', e)

    return sign, t

def get_taobao_sign_and_body(base_url, headers:dict, params:dict, data:json, timeout=13, _m_h5_tk='undefine', session=None):
    '''
    得到淘宝带签名sign接口数据
    :param base_url:
    :param headers:
    :param params:
    :param data:
    :param timeout:
    :param _m_h5_tk:
    :param session:
    :return: (_m_h5_tk, session, body)
    '''
    sign, t = calculate_right_sign(data=data, _m_h5_tk=_m_h5_tk)
    headers['Host'] = re.compile(r'://(.*?)/').findall(base_url)[0]
    params.update({     # 添加下面几个query string
        't': t,
        'sign': sign,
        'data': data,
    })

    if session is None:
        session = requests.session()
    else:
        session = session
    try:
        response = session.get(url=base_url, headers=headers, params=params, timeout=timeout)
        _m_h5_tk = response.cookies.get('_m_h5_tk', '')
        _m_h5_tk = _m_h5_tk.split('_')[0]
        # print(s.cookies.items())
        # print(_m_h5_tk)

        body = response.content.decode('utf-8')
        # print(body)

    except Exception as e:
        print('遇到错误:', e)
        _m_h5_tk = ''
        body = ''

    return (_m_h5_tk, session, body)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'h5api.m.taobao.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',      # 随机一个请求头
}

data = json.dumps({
    'bizCode': 'tejia_004',
    'currentPage': 1,
    'optStr': json.dumps({
        'priceScope': {     # 切记: priceScope这里不需要json.dumps, 否则请求不到数据
            "lowerLimit":1,
            "upperLimit":9999,
        },
        'category': ["495000"],
        'includeForecast': 'false',
        'topItemIds': [],
    }),
    'pageSize': 20,
    'salesSites': 9,
})

params = {
    "jsv": "2.4.8",
    "appKey": "12574478",
    # "t": t,
    # "sign": sign,
    "api": "mtop.ju.data.get",
    "v": "1.0",
    "type": "jsonp",
    "dataType": "jsonp",
    "callback": "mtopjsonp4",
    "data": data,
}

base_url = 'https://h5api.m.taobao.com/h5/mtop.ju.data.get/1.0/'
result_1 = get_taobao_sign_and_body(base_url=base_url, headers=headers, params=params, data=data)
_m_h5_tk = result_1[0]
# print(_m_h5_tk)
# 带上_m_h5_tk, 和之前请求返回的session再次请求得到需求的api数据
result_2 = get_taobao_sign_and_body(base_url=base_url, headers=headers, params=params, data=data, _m_h5_tk=_m_h5_tk, session=result_1[1])
body = result_2[2]
# print(body)

try:
    body = re.compile(r'\((.*?)\)').findall(body)[0]
    data = json.loads(body)
    # pprint(data)
    print(data)
except:
    print('error_2')

# try:
#     base_url = 'https://h5api.m.taobao.com/h5/mtop.ju.data.get/1.0/'
#     # t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
#     # print(t)
#
#     s = requests.session()
#     response = s.get(url=base_url, params=params, headers=headers)
#     _m_h5_tk = response.cookies['_m_h5_tk']
#     _m_h5_tk = _m_h5_tk.split('_')[0]
#
#     print(response.text)
#     # print(s.cookies.items())
#     print(_m_h5_tk)
#
#     t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
#     e = _m_h5_tk + '&' + t + '&' + appKey + '&' + data
#     # 计算正确的sign
#     sign = js_parser.call('h', e)
#
#     params['t'], params['sign'] = t, sign
#
#     r = s.get(url=base_url, params=params, headers=headers, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
#     # print(r.content.decode('utf-8'))
# except:
#     print('error')



