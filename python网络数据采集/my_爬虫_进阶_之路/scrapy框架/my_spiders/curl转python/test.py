# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

import requests
from json import dumps
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.fz_driver import BaseDriver
from fzutils.internet_utils import _get_url_contain_params

cookies = {
    '_gscu_2116842793': '38032346hapx8711',
    '_gscbrs_2116842793': '1',
    'Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2': '1538032347,1538033641,1538036233',
    'Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2': '1538036233',
    '_gscs_2116842793': 't38036233ti43gd11|pv:1',
    'vjkl5': '452b08fde99ff271a1601a11831f77c020f8e29d',
}

headers = {
    'Origin': 'https://wenshu.court.gov.cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = {
  'Param': '案件类型:刑事案件',
  'Index': '1',
  'Page': '5',
  'Order': '法院层级',
  'Direction': 'asc',
  'vl5x': 'f83cc8fdec03895f73371c8d',
  'number': '/wen',
  'guid': '32e2007b-0fe8-8bc0d5ed-938a16027a01'
}

verify = '/Users/afa/Downloads/*courtgovcn.crt'
# verify = '/Users/afa/Downloads/DigiCertSHA2SecureServerCA.crt'
url = 'https://wenshu.court.gov.cn/List/ListContent'
response = requests.post(url=url, headers=headers, cookies=cookies, data=data, verify=verify)
print(response.text)