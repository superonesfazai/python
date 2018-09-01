# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.internet_utils import get_random_phone_ua
import requests

URL = 'http://m.gx8899.com/'
headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': get_random_phone_ua(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# response = requests.request("GET", url=URL, headers=headers, proxies={'http': 'http://' + '121.232.147.222:9000'})
# status_code = response.status_code
# body = response.content.decode('gb2312')
# print(body)
# print(status_code)

proxies = {
    'http': 'http://{}:{}'.format('18.64.147.93', 9000),
    'https': 'https://{}:{}'.format('18.64.147.93', 9000),
}

import requests

cookies = {
    'Hm_lvt_f8c1e4d81c965d1da79624c14b47f440': '1535770972,1535770982',
    'Hm_lpvt_f8c1e4d81c965d1da79624c14b47f440': '1535770982',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


response = requests.get('http://ip111.cn/', headers=headers, cookies=None, proxies=proxies)
print(response.content.decode('utf-8'))
