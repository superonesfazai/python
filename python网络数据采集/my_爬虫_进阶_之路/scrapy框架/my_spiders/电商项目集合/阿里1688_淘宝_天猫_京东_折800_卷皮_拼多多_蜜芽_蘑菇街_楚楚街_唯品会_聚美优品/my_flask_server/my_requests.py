# coding:utf-8

'''
@author = super_fazai
@File    : my_requests.py
@Time    : 2017/3/22 10:13
@connect : superonesfazai@gmail.com
'''

import requests
from random import randint
from my_ip_pools import MyIpPools
import re, gc, json, time
from pprint import pprint
from json import dumps, loads

__all__ = [
    'MyRequests',
]

class MyRequests(object):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_url_body(cls, url, headers:dict, params=None, cookies=None, had_referer=False):
        '''
        根据url得到body
        :param tmp_url:
        :return: '' 表示出错退出 | body 类型str
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        proxy = proxies['http'][randint(0, len(proxies) - 1)]

        tmp_proxies = {
            'http': proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        tmp_headers = headers
        tmp_headers['Host'] = re.compile(r'://(.*?)/').findall(url)[0]
        if had_referer:
            if re.compile(r'https').findall(url) != []:
                tmp_headers['Referer'] = 'https://' + tmp_headers['Host'] + '/'
            else:
                tmp_headers['Referer'] = 'http://' + tmp_headers['Host'] + '/'

        s = requests.session()
        try:
            if params is not None:
                response = s.get(url, headers=tmp_headers, params=params, cookies=cookies, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                print(response.url)
            else:
                response = s.get(url, headers=tmp_headers, proxies=tmp_proxies, cookies=cookies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            body = response.content.decode('utf-8')

            body = re.compile('\t').sub('', body)
            body = re.compile('  ').sub('', body)
            body = re.compile('\r\n').sub('', body)
            body = re.compile('\n').sub('', body)
            # print(body)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            body = ''

        return body

    @classmethod
    def post_url_body(cls, url, headers:dict, params:dict=None, data=None, had_referer=False):
        '''
        根据url得到body
        :return: '' 表示出错退出 | body 类型str
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        proxy = proxies['http'][randint(0, len(proxies) - 1)]

        tmp_proxies = {
            'http': proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        tmp_headers = headers
        tmp_headers['Host'] = re.compile(r'://(.*?)/').findall(url)[0]
        if had_referer:
            if re.compile(r'https').findall(url) != []:
                tmp_headers['Referer'] = 'https://' + tmp_headers['Host'] + '/'
            else:
                tmp_headers['Referer'] = 'http://' + tmp_headers['Host'] + '/'

        s = requests.session()
        try:
            if params is not None:
                response = s.post(url, headers=tmp_headers, params=params, data=data, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            else:
                response = s.post(url, headers=tmp_headers, data=data, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            body = response.content.decode('utf-8')

            body = re.compile('\t').sub('', body)
            body = re.compile('  ').sub('', body)
            body = re.compile('\r\n').sub('', body)
            body = re.compile('\n').sub('', body)
            # print(body)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            body = ''

        return body

    def __del__(self):
        gc.collect()

def test():
    # 抓包: 唯品会微信小程序
    url = 'https://m.vip.com/server.html'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':	'gzip',
        'Accept-Language': 'zh-cn',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'm.vip.com',
        'Referer': 'https://servicewechat.com/wxe9714e742209d35f/284/page-frame.html',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/6.6.5 NetType/WIFI Language/zh_CN',
    }

    t = str(time.time().__round__()) + str(randint(100, 999))
    params = {
        'serv':	'getGoodsActiveMsg',
        '_xcxid': t,
    }

    goods_id = '460143743'
    page = 'product-0-' + str(goods_id) + '.html'
    data = dumps([
        {
            "method":"getGoodsActiveMsg",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025335,
            'id': 1,
            "jsonrpc":"2.0"
        },{
            "method":"getCoupon",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025336,
            'id': 2,
            "jsonrpc":"2.0"
        },{
            "method":"getProductDetail",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025337,
            'id': 3,
            "jsonrpc":"2.0"
        },{
            "method":"getProductMeta",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025338,
            'id': 4,
            "jsonrpc":"2.0"
        },{
            "method":"getProductSlide",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025339,
            'id': 5,
            "jsonrpc":"2.0"
        },{
            "method":"getProductMultiColor",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025340,
            'id': 6,
            "jsonrpc":"2.0"
        },{
            "method":"getProductSize",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025341,
            'id': 7,
            "jsonrpc":"2.0"
        },{
            "method":"getProductCountdown",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025342,
            'id': 8,
            "jsonrpc":"2.0"
        },{
            "method":"ProductRpc.getProductLicense",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025343,
            'id': 9,
            "jsonrpc":"2.0"
        },
    ])

    body = MyRequests.post_url_body(url=url, headers=headers, params=params, data=data)
    # print(body)
    try:
        data = json.loads(body)
        pprint(data)
    except:
        pass

    # body = MyRequests().get_url_body(url=url, headers=headers, params=params)
    # print(body)

# test()
