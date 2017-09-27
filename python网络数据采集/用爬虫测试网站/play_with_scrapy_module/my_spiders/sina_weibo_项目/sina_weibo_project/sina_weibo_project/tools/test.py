# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/9/26 12:00
@connect : superonesfazai@gmail.com
'''

from scrapy.http import Request
from urllib.request import urlopen
import requests
from pprint import pprint
import json
from random import randint

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=utf-8',
    'Host': 'd.weibo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'cookie': 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; wvr=6; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; login_sid_t=6c2521139641765552eaeffdc3bc61bb; cross_origin_proto=SSL; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; _s_tentry=login.sina.com.cn; UOR=developer.51cto.com,widget.weibo.com,www.google.com.hk; Apache=5561465425422.705.1506498709692; ULV=1506498709703:7:4:1:5561465425422.705.1506498709692:1506162530082; SSOLoginState=1506498732; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHYuqSfdfkuLvgn1Aleex5zsmmnegsTlkWruzgTjSBrPw.; SUB=_2A250zyj_DeRhGeNM41sX8ybLzjmIHXVXvR03rDV8PUNbmtBeLWfskW9ZsO0IUPFMAeSGgnp47TqH60IC6g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=0RyqLwWNEb6XCS; ALF=1538034730; un=15661611306; wb_cusLike_5289638755=N; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295'
}
# 1506471533330
# _rnd = str(150647) + str(1000000)

# _rnd = str(1506471533330)

domain = '102803_ctg1_{}_-_ctg1_{}'.format(str(6288), str(6288))
id = domain
pagebar = str(0)
current_page = str(1)
script_uri = r'/102803_ctg1_{}_-_ctg1_{}'.format(str(6288), str(6288))
domain_op = domain
# __rnd = str(1506471533330)
__rnd = str(1506494189805)
url = 'https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&from=faxian_hot&mod=fenlei&tab=home&pre_page=1&page=1&pl_name=Pl_Core_NewMixFeed__3&feed_type=1&domain={}&pagebar={}&current_page={}&id={}&script_uri={}&domain_op={}&__rnd={}'\
    .format(domain, pagebar, current_page, id, script_uri, domain_op, __rnd)

# proxies = {
#     'http': 'http://123.147.165.144:80',
# }

tmp_proxies = {
    'http': [
        'http://123.147.165.144:80',
        'http://111.53.65.92:8080',
    ]
}

proxies = {
    'http': tmp_proxies['http'][randint(0, 1)]
}

# response = requests.get(url, headers=headers, proxies=proxies).json()       # 用requests自带的json就很好用
# content = json.loads(response.text)     # json返回的数据进行转码为dict格式, 顺带识别里面的文字
# print(response.text)        # 报 File not found.的错
# print(type(response))
# print(response['data'])
# print(len(response['data']))
# print(content['data'])
# print(response.encoding)
print(proxies)

a = u'\u5206\u5272\u7ebf'
b = u'\u8bdd\u9898page\u9875\u9762\u8fd4\u56de\u4e3a\u7a7a\u65f6\u5e76\u4e14\u4e0d\u662f\u6700\u540e\u4e00\u4e2a\u5206\u5c4f\u65f6\u7ee7\u7eed\u52a0\u8f7d'
print(eval('u\'' + a + '\''))
print(eval('u\'' + b + '\''))