# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.internet_utils import get_random_pc_ua
import requests

def baidu_check(ip, port):
    '''用百度: 验证proxy可用性'''
    url = "https://www.baidu.com/"
    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "no-cache",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': get_random_pc_ua(),
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
    }
    response = requests.request("GET", url, headers=headers, proxies={'http': 'http://{}:{}'.format(ip, port)})
    body = response.content.decode('utf-8')

    return body

# print(baidu_check(ip='180.118.135.149', port=9000))

