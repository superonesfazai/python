# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

import re
from random import choice
from requests import get
from requests.exceptions import (
    ConnectTimeout,
    ReadTimeout,
    ProxyError,
    SSLError,)
from chardet import detect

from api import IpPoolsObj

from fzutils.internet_utils import get_random_pc_ua
from fzutils.common_utils import json_2_dict

headers = {
    'Connection': "keep-alive",
    'Cache-Control': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': get_random_pc_ua(),
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
}

def proxy_ip_check(url, headers, ip, port):
    '''验证proxy可用性'''
    proxies = {
        'http': 'http://{}:{}'.format(ip, port),
        'https': 'http://{}:{}'.format(ip, port),
    }
    body = ''
    try:
        response = get(url, headers=headers, proxies=proxies, timeout=8)
        # try:
        #     body = response.content.decode(response.encoding or detect(response.content).get('encoding'))
        # except:
        #     body = response.text
        body = response.text

    except (ConnectTimeout, ReadTimeout, ProxyError, SSLError) as e:
        # print('遇到错误: ', e.args[0])
        pass

    except Exception as e:
        print('遇到错误: ', e.args[0])

    return body

# _ = IpPoolsObj()
# h_proxys = _._get_all_ip_proxy()
# # print(h_proxys)
#
# # url = 'https://www.baidu.com'
# url = 'http://httpbin.org/get'
#
# h_proxys_len = len(h_proxys)
# success_num = 0
# for i in h_proxys:
#     one = choice(h_proxys)
#     ip = one.get('ip')
#     port = one.get('port')
#     body = proxy_ip_check(url=url, headers=headers, ip=ip, port=port)
#     # print(body)
#     res = json_2_dict(body)
#     origin = res.get('origin', '')
#     if origin != '':
#         print('[+] {}:{}'.format(ip, port))
#         success_num += 1
#     else:
#         print('[-] {}:{}'.format(ip, port))
#
# print('成功率:{}%'.format(success_num/h_proxys_len*100))