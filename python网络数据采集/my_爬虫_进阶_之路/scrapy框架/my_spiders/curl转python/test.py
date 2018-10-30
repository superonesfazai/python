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
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'Host': 'news.app.autohome.com.cn',
    # 'apisign': '1|199c27eea0a0c4085e6650d68f01730eeadacda1|autohomebrush|1540894009|C8E6305EE3E520EEC7FA64ED3BBAF6F2',
    'User-Agent': 'iPhone\t11.0\tautohome\t9.6.0\tiPhone',
}

params = (
    ('pm', '1'),
    ('cityid', '330100'),
    ('newstype', '0'),
    ('subjectids', ''),
    ('bi', '1'),
    ('uid', ''),
    # ('devid', '199c27eea0a0c4085e6650d68f01730eeadacda1'),
    ('op', '1'),
    ('net', '5'),
    ('gps', '30.190538,120.201477'),
    ('lasttime', '0'),
    ('isonline', '1'),
    ('version', '9.6.0'),
    ('showfocusimg', '1'),
    # ('bsdata', 'eyJSZW1haW5EcUxlbiI6MCwicHZvcmRpbmEiOjMsInB2VGltZSI6MTU0MDg5MzYzN30='),
    ('ratio', '-1'),
    ('restart', '0'),
    ('pagesize', '0'),
    ('ischeck', '0'),
    ('idfa', 'DA8C3A83-C08C-4881-86A8-1E67849F5BB2'),       # 定值
    ('os_version', '11.0'),
    ('rnversion', '1.3.2'),
    ('abtest', 'ios_homepagechangestyle,new;ios_homepagechangedata,old;'),
)
# 常规ip池无用, 可以自己构建都太dasl拨号vps, 实现抓取
# shouye.as
data = json_2_dict(requests.get('https://222.42.5.34/shouye_v8.9.0/news/shouye.ashx', headers=headers, params=params, cookies=None, verify=False).text)
pprint(data)
