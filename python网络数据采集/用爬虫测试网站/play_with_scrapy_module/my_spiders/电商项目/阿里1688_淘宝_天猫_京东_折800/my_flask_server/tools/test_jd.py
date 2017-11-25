# coding:utf-8

'''
@author = super_fazai
@File    : test_jd.py
@Time    : 2017/11/10 13:36
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import requests
from time import sleep
from pprint import pprint
import pytz
import datetime
import re
import requests

goods_id = '17983261076'
# url = 'https://item.m.jd.com/ware/detail.json?wareId=' + goods_id
# url = 'https://mitem.jd.hk/cart/cartNum.json'
url = 'https://m.yiyaojd.com/ware/getSpecInfo.json?wareId='

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Host': 'item.m.jd.com',
    # 'Host': 'mitem.jd.hk',
    'Host': 'm.yiyaojd.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',      # 随机一个请求头
}

response = requests.get(url, headers=headers)
pprint(response.content.decode('utf-8'))
# print(str(response.cookies.get('sid')))


