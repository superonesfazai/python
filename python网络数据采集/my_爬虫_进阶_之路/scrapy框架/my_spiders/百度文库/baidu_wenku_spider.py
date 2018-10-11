# coding:utf-8

'''
@author = super_fazai
@File    : baidu_wenku_spider.py
@connect : superonesfazai@gmail.com
'''

"""
百度文库爬虫
"""

import requests

headers = {
    'Referer': 'http://youke.baidu.com/course/preview/2d495b8102d276a200292e7f?fr=undefined',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
params = (
    ('responseCacheControl', 'max-age=3888000'),
    # ('responseExpires', 'Sun, 25 Nov 2018 14:46:19 +0800'),
    # ('authorization', 'bce-auth-v1/fa1126e91489401fa7cc85045ce7179e/2018-10-11T06:46:19Z/3600/host/e829dc2f109e31d23298256bcf1ad55f7d10fe88a4ea5ad688b9bdeb653795e2'),
    ('x-bce-range', '66628-84608'),     # aaa-xxx 文档内容范围 最开始为0
    ('token', '970ed4d0a88916318d4273523b6848cb4f1e3f475aaf27ad828cb3330c09e469'),  # * 单个doc文档的实际内容在[wkbjbos.bdimg.com.*0.json这个接口中, token值在网页原页面html中]
    ('expire', '2018-10-11T07:46:19Z'),
)

response = requests.get('http://wkbjbos.bdimg.com/v1/docconvert6125//wk/9c2223edabe07bb191508859274bb616/0.json', headers=headers, params=params)
print(response.text)