# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from __future__ import unicode_literals

from ftfy import fix_text
from random import randint
from urllib.parse import (
    urlparse,
    parse_qsl,
    urlencode,)
from fzutils.ip_pools import (
    fz_ip_pool,
    ip_proxy_pool,
    sesame_ip_pool,
    tri_ip_pool,
    get_random_proxy_ip_from_ip_pool,)
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
from fzutils.spider.fz_requests import (
    PROXY_TYPE_HTTP,
    PROXY_TYPE_HTTPS,)
from fzutils.spider.selector import *
from fzutils.spider.async_always import *
from fzutils.spider.selenium_always import *

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

# 源自百家号
# 百度某作者的文章
# 必传
# cookies = {
#     'BAIDUID': '1666ADBB95B083DBB2DA29E9BEFCB50B:FG=1',
#     'BIDUPSID': '1666ADBB95B083DBB2DA29E9BEFCB50B',
#     # 'PSTM': '1553750958',
#     # 'locale': 'zh',
# }
#
# headers = {
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#     'User-Agent': get_random_phone_ua(),
#     'Accept': '*/*',
#     # 'Referer': 'https://author.baidu.com/home?type=profile&action=profile&mthfr=box_share&context=%7B%22from%22%3A%22ugc_share%22%2C%22app_id%22%3A%221617808623102717%22%7D&from=singlemessage&isappinstalled=0',
#     'Connection': 'keep-alive',
# }
#
# params = (
#     ('type', 'article'),
#     ('tab', '2'),
#     ('uk', 'sCWQteHJevYiu1bvIiKrEw'),           # 非定值, 看分享出来文章的uk
#     # ('ctime', '15564325069740'),
#     ('num', '14'),
#     # ('_', '1556502637335'),
#     ('callback', 'jsonp2'),
# )
# url = 'https://author.baidu.com/list'
# body = Requests.get_url_body(
#     url=url,
#     headers=headers,
#     params=params,
#     cookies=cookies,
#     ip_pool_type=tri_ip_pool,)
# # print(body)
#
# data = json_2_dict(
#     json_str=re.compile('\((.*)\)').findall(body)[0],
# )
# pprint(data)

# 视频信息接口
# params = (
#     ('callback', 'tvp_request_getinfo_callback_654434'),
#     ('platform', '11001'),
#     ('charge', '0'),
#     ('otype', 'json'),
#     ('ehost', 'http://post.mp.qq.com'),
#     ('sphls', '0'),
#     ('sb', '1'),
#     ('nocache', '0'),
#     # ('_rnd', '1557917186'),
#     # ('guid', 'daf25a829d645f1196b61df6417e87bf'),
#     ('appVer', 'V2.0Build9502'),
#     ('vids', 'm0866r0q1xn'),
#     ('defaultfmt', 'auto'),
#     # ('_qv_rmt', 'AI5PT6eoA15978I5x='),
#     # ('_qv_rmt2', 'Kt7fT8OE157116tsw='),
#     ('sdtfrom', 'v3010'),
#     ('_', '1557917186891'),
# )

# body = Requests.get_url_body(
#     url='http://h5vv.video.qq.com/getinfo',
#     headers=headers,
#     params=params,
#     ip_pool_type=tri_ip_pool,
#     num_retries=5,)
# print(body)
# data = json_2_dict(
#     json_str=re.compile('\((.*)\)').findall(body)[0],
#     default_res={})
# pprint(data)

# 咪咕视频根据视频id进行视频信息获取
# import requests
#
# headers = {
#     'Proxy-Connection': 'keep-alive',
#     'terminalId': 'h5',
#     # 'X-UP-CLIENT-CHANNEL-ID': '0131_10010001005',
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
#     'Accept': 'application/json',
#     # 'clientId': '36854075131aeac30ca17f1b54649196',
#     'userId': '',
#     'userToken': '',
#     'appId': 'miguvideo',
#     'SDKCEId': '',
#     'Origin': 'http://m.miguvideo.com',
#     'Referer': 'http://m.miguvideo.com/mgs/msite/prd/detail.html?cid=652525090',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
# }
#
# params = (
#     ('contId', '652525090'),
#     ('rateType', '3'),
#     # ('clientId', '36854075131aeac30ca17f1b54649196'),
#     # ('channelId', '0131_10010001005'),
# )
#
# response = requests.get('http://webapi.miguvideo.com/gateway/playurl/v2/play/playurlh5', headers=headers, params=params, verify=False)
# print(response.text)