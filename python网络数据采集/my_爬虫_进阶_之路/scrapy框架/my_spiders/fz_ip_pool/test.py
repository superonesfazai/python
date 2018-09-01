# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.internet_utils import get_random_phone_ua
import requests

proxies = {
    'http': 'http://{}:{}'.format('183.129.244.15', 10010),
    'https': 'https://{}:{}'.format('18.64.147.93', 9000),
}

cookies = {
    '_gauges_unique_month': '1',
    '_gauges_unique_year': '1',
    '_gauges_unique': '1',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

response = requests.get('http://httpbin.org/get', headers=headers, cookies=None, proxies=None)
print(response.content.decode('utf-8'))
