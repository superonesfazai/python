# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

import re
from scrapy.selector import Selector
from time import sleep
from pprint import pprint

from fzutils.spider.fz_requests import Requests, fz_ip_pool, ip_proxy_pool, sesame_ip_pool
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.fz_driver import BaseDriver, CHROME
from fzutils.spider.fz_phantomjs import CHROME_DRIVER_PATH
from fzutils.internet_utils import *
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import *
from fzutils.common_utils import get_random_int_number
from fzutils.url_utils import unquote_plus

import requests

headers = {
    'authority': 'item.jd.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'if-modified-since': 'Mon, 12 Nov 2018 09:56:40 GMT',
}

response = requests.get('https://item.jd.com/20337503932.html', headers=headers)
print(response.text)