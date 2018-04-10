# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2018/4/9 17:04
@connect : superonesfazai@gmail.com
'''
import sys, json, re
sys.path.append('..')
from pprint import pprint

from my_requests import MyRequests
from my_phantomjs import MyPhantomjs

import requests

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'accept': '*/*',
    'referer': 'https://item.taobao.com/item.htm?id=555635098639',
    # 'cookie': 't=5de7bdbe0c944c70edf42507df48b7d4; cna=nGIlE3QL1ksCAX145epTBk9n; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tg=0; enc=XbQN9%2FZ5BOjIMJ3%2BNpNGywfaXkDB2IiEdebYnFvLS2XEPMDl4crrCuln1oh3edcjZ4wsm9o%2FHZLwUPUfPALCKQ%3D%3D; uc3=nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBz4WxXQovmTd8Kcs%3D&lg2=UIHiLt3xD8xYTw%3D%3D; _cc_=URm48syIZQ%3D%3D; UM_distinctid=1623368af544cc-0c911cd96f128e-33627805-fa000-1623368af56536; _m_h5_tk=03ecbeb370c40a3b63ab6f111e91d906_1523331137595; _m_h5_tk_enc=942da43f92e0bd95235a4dab76e02869; mt=ci=-1_0; v=0; cookie2=255188c1941b04517699509e72e362e2; _tb_token_=e1f09e5e3e7bb; uc1=cookie14=UoTePTbFynm3jw%3D%3D; isg=BNXVDV2YI9jrtAf3RM7mJmGC5NdPeolUrx5MR1d6cs6XrvegHyIWtHosfLIYrqGc',
}

params = (
    ('auctionNumId', '555635098639'),
    # ('userNumId', '1681172037'),
    ('currentPageNum', '1'),
    ('pageSize', '20'),
    ('rateType', '1'),
    ('orderType', 'sort_weight'),
    ('attribute', ''),
    ('sku', ''),
    ('hasSku', 'false'),
    ('folded', '1'),        # 把默认的0改成1能得到需求数据
    # ('ua', '098#E1hv1QvWvRGvUpCkvvvvvjiPPFMWAjEmRLdWlj1VPmPvtjEvnLsh1j1WR2cZgjnVRT6Cvvyv9VliFvmvngJjvpvhvUCvp2yCvvpvvhCv2QhvCPMMvvvCvpvVvUCvpvvvKphv8vvvpHwvvvmRvvCmDpvvvNyvvhxHvvmChvvvB8wvvUVhvvChiQvv9OoivpvUvvCCUqf1csREvpvVvpCmpaFZmphvLv84Rs+azCIajCiABq2XrqpAhjCbFO7t+3vXwyFEDLuTRLa9C7zhVTTJhLhL+87J+u0OakSGtEkfVCl1pY2ZV1OqrADn9Wma+fmtEp75vpvhvvCCBUhCvCiI712MPY147DSOSrGukn22SYHsp7uC6bSVksyCvvpvvhCv'),
    # ('_ksTS', '1523329154439_1358'),
    # ('callback', 'jsonp_tbcrate_reviews_list'),
)

response = requests.get('https://rate.taobao.com/feedRateList.htm', headers=headers, params=params)
body = response.content.decode('gbk')
# print(body)

try:
    body = re.compile('\((.*)\)').findall(body)[0]
except IndexError:
    print('IndexError')
try:
    data = json.loads(body).get('comments', [])
    pprint(data)
    print(len(data))
except:
    print('error')
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://rate.taobao.com/feedRateList.htm?auctionNumId=555635098639&userNumId=1681172037&currentPageNum=1&pageSize=20&rateType=1&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098%23E1hv1QvWvRGvUpCkvvvvvjiPPFMWAjEmRLdWlj1VPmPvtjEvnLsh1j1WR2cZgjnVRT6Cvvyv9VliFvmvngJjvpvhvUCvp2yCvvpvvhCv2QhvCPMMvvvCvpvVvUCvpvvvKphv8vvvpHwvvvmRvvCmDpvvvNyvvhxHvvmChvvvB8wvvUVhvvChiQvv9OoivpvUvvCCUqf1csREvpvVvpCmpaFZmphvLv84Rs%2BazCIajCiABq2XrqpAhjCbFO7t%2B3vXwyFEDLuTRLa9C7zhVTTJhLhL%2B87J%2Bu0OakSGtEkfVCl1pY2ZV1OqrADn9Wma%2BfmtEp75vpvhvvCCBUhCvCiI712MPY147DSOSrGukn22SYHsp7uC6bSVksyCvvpvvhCv&_ksTS=1523329154439_1358&callback=jsonp_tbcrate_reviews_list', headers=headers)
