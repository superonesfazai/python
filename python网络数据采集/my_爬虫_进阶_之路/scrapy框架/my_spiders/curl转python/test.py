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

# ** 咪咕视频根据视频id进行视频信息获取
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

# 百度app的小视频发现接口, 其中的全屏视频文章可直接被抓取
# headers = {
#     'Host': 'mbd.baidu.com',
#     'Connection': 'keep-alive',
#     'Content-Length': '4557',
#     'X-BD-QUIC': '1',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'X-BDBoxApp-NetEngine': '3',
#     'User-Agent': get_random_phone_ua(),   # 'Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.18.0'
#     # 'X-Bd-Traceid': '644a9f61e6cc425e8df842d2cb926de9',
#     'Accept': '*/*',
#     # 'X-TurboNet-Info': '2.13.2679.177',
#     'Accept-Encoding': 'gzip, deflate',
# }
#
# params = (
#     ('action', 'feed'),
#     ('cmd', '210'),
#     # ('maid', '_a2S8_aq28_qa28qiPSOtj8Pvag3h2aajiXT8jukvNlza-uNzuB3uli6-u_KO-ifY0HJ8lukSugkuXa90ivhI_PSv8oIi2ihgCSaa_asS8_M82uazxqSC'),
#     ('refresh', '1'),
#     ('imgtype', 'webp'),
#     ('cfrom', '1099a'),
#     ('from', '1099a'),
#     ('network', '1_0'),
#     ('osbranch', 'i0'),
#     ('osname', 'baiduboxapp'),
#     ('service', 'bdbox'),
#     # ('sid', '1027585_4-2600_6645-1027088_2-1027514_1-1027521_1-1027598_3-3081_8171-5238_7311-2696_6930-1027056_2-3057_8089-5618_8591-1027583_1-1027195_1-1027384_2-1027255_3-1027604_1-5456_8016-1026924_1-5306_7565-1027258_2-3270_8882-2946_7781-1027230_2-5524_8269-1027659_1-2929_7702-1027285_1-1027328_5-1027599_1-1472_3438-5579_8458-3037_8036-1027425_3-1027641_1-1027564_2-3000026_2-1027249_1-1027654_1-1027525_2-5529_8280-1027151_2-5566_8411-1027577_2-5562_8387-1027102_1-5571_8441-1027346_1-1021859_1-5409_7877-3039_8040-5586_8486-5546_8581-1027597_2-1027562_1-1027251_1-5525_8271-1021774_1-2512_6387-2859_7452-1027460_2-1027128_2-1027379_1-1027652_2-2939_7745-1027218_1-1027225_1-1026985_1'),
#     ('sst', '0'),
#     ('st', '0'),
#     ('ua', '1668_2224_iphone_11.22.0.17_0'),
#     ('uid', 'E4317D7927A4F423B2A894710C308D015F8D69D51OMTBGHBERB'),
#     # ('ut', 'iPad7,3_13.3.1'),
#     # ('zid', '9iAc0yzbau51GKO563M1gzHzaPoPDD_d8nXwjCKxdBLITCmV4uqwJmkYrkuarE6BQqUXF7INisVWgScgYhwZ0qQ'),
# )
#
# data = {
#   # 'data': '{\n  "upload_ids" : [\n    {\n      "clk" : 0,\n      "id" : "sv_5653763656459563687",\n      "show" : 0,\n      "clk_ts" : 0,\n      "show_ts" : 0\n    },\n    {\n      "clk" : 0,\n      "id" : "sv_3599925748637729943",\n      "show" : 0,\n      "clk_ts" : 0,\n      "show_ts" : 0\n    },\n    {\n      "clk" : 0,\n      "id" : "sv_5250727945753531281",\n      "show" : 0,\n      "clk_ts" : 0,\n      "show_ts" : 0\n    },\n    {\n      "clk" : 0,\n      "id" : "sv_4823468498756614746",\n      "show" : 1,\n      "clk_ts" : 0,\n      "show_ts" : 1587165880\n    },\n    {\n      "clk" : 0,\n      "id" : "sv_4439062174156612467",\n      "show" : 1,\n      "clk_ts" : 0,\n      "show_ts" : 1587165886\n    },\n    {\n      "clk" : 0,\n      "id" : "sv_5248424962721750237",\n      "show" : 1,\n      "clk_ts" : 0,\n      "show_ts" : 1587165886\n    },\n    {\n      "clk" : 0,\n      "id" : "sv_4130330140644084020",\n      "show" : 1,\n      "clk_ts" : 0,\n      "show_ts" : 1587165880\n    },\n    {\n      "clk" : 0,\n      "id" %3...'
#     'data': dumps({
#     "upload_ids" : [
#         {
#           "clk" : 0,
#           "id" : "sv_5653763656459563687",
#           "show" : 0,
#           "clk_ts" : 0,
#           "show_ts" : 0
#         },
#         {
#           "clk" : 0,
#           "id" : "sv_3599925748637729943",
#           "show" : 0,
#           "clk_ts" : 0,
#           "show_ts" : 0
#         },
#         {
#           "clk" : 0,
#           "id" : "sv_5250727945753531281",
#           "show" : 0,
#           "clk_ts" : 0,
#           "show_ts" : 0
#         },
#         {
#           "clk" : 0,
#           "id" : "sv_4823468498756614746",
#           "show" : 1,
#           "clk_ts" : 0,
#           "show_ts" : datetime_to_timestamp(get_shanghai_time()),   # 1587165880
#         },
#         {
#           "clk" : 0,
#           "id" : "sv_4439062174156612467",
#           "show" : 1,
#           "clk_ts" : 0,
#           "show_ts" : datetime_to_timestamp(get_shanghai_time())
#         },
#         {
#           "clk" : 0,
#           "id" : "sv_5248424962721750237",
#           "show" : 1,
#           "clk_ts" : 0,
#           "show_ts" : datetime_to_timestamp(get_shanghai_time())
#         },
#         {
#           "clk" : 0,
#           "id" : "sv_4130330140644084020",
#           "show" : 1,
#           "clk_ts" : 0,
#           "show_ts" : datetime_to_timestamp(get_shanghai_time())
#         },
#     ]})
# }
# body = Requests.get_url_body(
#     method='post',
#     url='https://mbd.baidu.com/searchbox',
#     headers=headers,
#     params=params,
#     # cookies=cookies,
#     data=data,
#     ip_pool_type=tri_ip_pool,
#     proxy_type=PROXY_TYPE_HTTPS,
#     num_retries=6,)
# data = json_2_dict(
#     json_str=body).get('data', {}).get('210', {}).get('itemlist', {}).get('items', [])
# # pprint(data)
#
# for item in data:
#     try:
#         _mode = item.get('data', {}).get('mode', '')
#         assert _mode != ''
#         title = item.get('data', {}).get('title', '')
#         assert title != ''
#         article_url = item.get('data', {}).get('videoInfo', {}).get('pageUrl', '')
#         print('mode: {}, title: {}, article_url: {}'.format(_mode, title, article_url))
#     except Exception:
#         continue