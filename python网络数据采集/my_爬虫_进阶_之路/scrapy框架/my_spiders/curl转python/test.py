# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from __future__ import unicode_literals

from ftfy import fix_text
from random import randint
from urllib.parse import urlencode
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

# headers = {
#     'Accept-Encoding': 'br, gzip, deflate',
#     'Connection': 'keep-alive',
#     'Accept': '*/*',
#     'Host': 'alisitecdn.m.taobao.com',
#     'User-Agent': 'iPhone7,1(iOS/11.0) AliApp(TB/8.4.0) Weex/0.20.0 1242x2208',
#     'Accept-Language': 'zh-cn',
# }
#
# params = (
#     ('pathInfo', 'shop/impression'),
#     ('userId', '3012445016'),
#     ('shopId', '380157209'),
#     ('pageId', '0'),
# )
# url = 'https://alisitecdn.m.taobao.com/pagedata/shop/impression'
# body = Requests.get_url_body(
#     url=url,
#     headers=headers,
#     params=params,
#     cookies=None,
#     ip_pool_type=tri_ip_pool)
# # print(body)
# data = json_2_dict(body)
# # pprint(data)
# # 服务电话的js
# print(data.get('module', {}).get('moduleSpecs', {}).get('shop_base_info', {}).get('moduleCode', ''))

headers = {}
params = (
    ('q', '裤子'),
    ('sourcePage', '/goods'),
    ('page_no', '1'),
)
url = 'http://www.huoniuniu.com/goods'
body = Requests.get_url_body(
    url=url,
    headers=headers,
    params=params,
    num_retries=6,
    ip_pool_type=tri_ip_pool,)
# print(body)

shop_item_selector = {
    'method': 'css',
    'selector': 'div.ps-item1 div.shopname_box a.shopname.max_width ::attr("href")',
}
shop_id_selector = {
    'method': 're',
    'selector': '\/shop\/(\d+)',
}
shop_item_list = parse_field(
    parser=shop_item_selector,
    target_obj=body,
    is_first=False,
)
# pprint(shop_item_list)

shop_id_list = []
for item in shop_item_list:
    try:
        company_id = parse_field(
            parser=shop_id_selector,
            target_obj=item,
            is_first=True,)
        assert company_id != '', 'company_id不为空值!'
        shop_id_list.append({
            'company_id': company_id
        })
    except AssertionError:
        continue
shop_id_list = list_remove_repeat_dict_plus(
    target=shop_id_list,
    repeat_key='company_id',)
pprint(shop_id_list)