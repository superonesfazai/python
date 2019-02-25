# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from __future__ import unicode_literals

from ftfy import fix_text
from fzutils.ip_pools import (
    fz_ip_pool,
    ip_proxy_pool,
    sesame_ip_pool,
    tri_ip_pool,)
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.fz_driver import (
    BaseDriver, 
    CHROME,)
from fzutils.spider.fz_phantomjs import CHROME_DRIVER_PATH
from fzutils.url_utils import unquote_plus
from fzutils.img_utils import save_img_through_url
from fzutils.spider.fz_driver import PHONE
from fzutils.common_utils import _print
from fzutils.data.excel_utils import read_info_from_excel_file
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.internet_utils import str_cookies_2_dict
from fzutils.spider.selector import *
from fzutils.spider.async_always import *

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': get_random_pc_ua(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
url = 'http://www.yiwugo.com/hu/021784703.html'
body = Requests.get_url_body(
    url=url,
    headers=headers,
    cookies=None,
    ip_pool_type=tri_ip_pool,
    num_retries=6)
print(body)

# headers = {
#     'Host': 'alisitecdn.m.taobao.com',
#     'Accept': '*/*',
#     'User-Agent': 'iPhone7,1(iOS/11.0) AliApp(TB/8.4.0) Weex/0.20.0 1242x2208',
#     'Accept-Language': 'zh-cn',
# }
#
# params = (
#     ('pathInfo', 'shop/impression'),
#     ('userId', '665575899'),
#     ('shopId', '72260783'),
#     ('pageId', '0'),
# )
# url = 'https://alisitecdn.m.taobao.com/pagedata/shop/impression'
# body = Requests.get_url_body(
#     url=url,
#     headers=headers,
#     params=params,
#     ip_pool_type=tri_ip_pool
# )
# # print(body)
# data = json_2_dict(body)
# pprint(data)

