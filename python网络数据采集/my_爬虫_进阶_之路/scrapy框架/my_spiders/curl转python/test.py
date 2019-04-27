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
    CHROME,
    FIREFOX,)
from fzutils.spider.fz_phantomjs import CHROME_DRIVER_PATH
from fzutils.url_utils import unquote_plus
from fzutils.img_utils import save_img_through_url
from fzutils.spider.fz_driver import PHONE
from fzutils.common_utils import _print
from fzutils.data.excel_utils import read_info_from_excel_file
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.internet_utils import (
    str_cookies_2_dict,
    _get_url_contain_params,
    tuple_or_list_params_2_dict_params,
    driver_cookies_list_2_str,)
from fzutils.qrcode_utils import decode_qrcode
from fzutils.spider.selector import *
from fzutils.spider.async_always import *

FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

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
# data = json_2_dict(
#     json_str=body,
#     default_res={}).get('module', {})
# # pprint(data)
# # 服务电话的js
# # print(data.get('module', {}).get('moduleSpecs', {}).get('shop_base_info', {}).get('moduleCode', ''))
#
# def wash_ori_data(ori_data:dict):
#     """
#     清洗原始data
#     :return:
#     """
#     try:
#         ori_data.pop('moduleSpecs')
#         ori_data.pop('moduleList')
#     except:
#         pass
#
#     return ori_data
#
# data = wash_ori_data(ori_data=data)
# pprint(data)

# wireshark
# iOS (ip.addr == 192.168.3.2 or ip.src == 192.168.3.2) and ssl
# meizu (ip.addr == 192.168.3.4 or ip.src == 192.168.3.4) and (ssl or http)

# charles
# https://campaigncdn.m.taobao.com/moduledata/downgrade.htm?dataId=taobao
# https://alisitecdn.m.taobao.com/pagedata/shop/index?pathInfo=shop/index&userId=201249601&shopId=58640118&pageId=1860970
# https://alisitecdn.m.taobao.com/pagedata/shop/impression?pathInfo=shop/impression&userId=201249601&shopId=58640118&pageId=0

# wireshark
# $ sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --ssl-key-log-file=/Users/afa/sslkeylog.log

# android (ip.addr == 192.168.3.4 or ip.src == 192.168.3.4) and ssl

# company_info
# headers = {
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': get_random_pc_ua(),
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     # 'Referer': 'http://z.go2.cn/product/oaamaeq.html',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
# }
# url = 'http://diteni.go2.cn/'
# body = Requests.get_url_body(
#     url=url,
#     headers=headers,
#     ip_pool_type=tri_ip_pool,)
# print(body)
#
# company_name_selector = {
#     'method': 'css',
#     'selector': 'a.merchant-title ::text'
# }
# company_name = parse_field(
#     parser=company_name_selector,
#     target_obj=body,
# )
# print(company_name)


