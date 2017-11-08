# coding:utf-8

'''
@author = super_fazai
@File    : ju_taobao_parse.py
@Time    : 2017/11/7 08:21
@connect : superonesfazai@gmail.com
'''

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import selenium.webdriver.support.ui as ui
# from selenium.webdriver.common.proxy import Proxy
# from selenium.webdriver.common.proxy import ProxyType
# from scrapy import Selector
# from urllib.request import urlopen
# from PIL import Image
from time import sleep
import datetime
import gc
# import pycurl
# from io import StringIO
# import traceback
# from io import BytesIO

from settings import HEADERS
from settings import PHANTOMJS_DRIVER_PATH, CHROME_DRIVER_PATH
import pytz

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

# chrome驱动地址
my_chrome_driver_path = CHROME_DRIVER_PATH

class JuTaobaoParse(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'acs.m.taobao.com',
            'User-Agent': HEADERS[randint(0, 34)]      # 随机一个请求头
        }
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data 类型dict
        '''
        """
        构造地址的参数:
        api:mtop.taobao.detail.getdetail
        ttid:2017@taobao_h5_6.6.0
        data:{"itemNumId":"44445349558"}
        appKey:12574478
        dataType:jsonp
        type:jsonp
        callback:define
        v:6.0
        """

        appKey = '12574478'

        # 下面构造params
        params_data = {
            'itemNumId': goods_id
        }
        params = {
            'data': json.dumps(params_data)  # 每层里面的字典都要先转换成json
        }

        tmp_url = "https://unszacs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appkey={}&api=mtop.taobao.detail.getdetail&ttid=2017@taobao_h5_6.6.0&dataType=jsonp&type=jsonp&callback=define&v=6.0".format(
            appKey,
        )

        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        try:
            response = requests.get(tmp_url, headers=self.headers, params=params, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
            # print(last_url)
            response = requests.get(last_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            data = response.content.decode('utf-8')
            print(data)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            return {}

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            if item[2] > 7:
                tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
                result_ip_list['http'].append(tmp_url)
            else:
                delete_url = 'http://127.0.0.1:8000/delete?ip='
                delete_info = requests.get(delete_url + item[0])
        # pprint(result_ip_list)
        return result_ip_list

    def get_goods_id_from_url(self, ju_url):
        is_ju_url = re.compile(r'https://detail.ju.taobao.com/home.htm.*?').findall(ju_url)
        if is_ju_url != []:
            if re.compile(r'https://detail.ju.taobao.com/home.htm.*?item_id=(\d+)&{0,20}.*?').findall(ju_url) != []:
                tmp_ju_url = re.compile(r'https://detail.ju.taobao.com/home.htm.*?item_id=(\d+)&{0,20}.*?').findall(ju_url)[0]
                # print(tmp_taobao_url)
                if tmp_ju_url != []:
                    goods_id = tmp_ju_url
                else:
                    ju_url = re.compile(r';').sub('', ju_url)
                    goods_id = re.compile(r'https://detail.ju.taobao.com/home.htm.*?item_id=(\d+)').findall(ju_url)[0]
                print('------>>>| 得到的淘宝商品id为:', goods_id)
                return goods_id
            else:       # 处理存数据库中取出的如: https://detail.ju.taobao.com/home.htm?item_id=560164926470
                print('9999')
                ju_url = re.compile(r';').sub('', ju_url)
                goods_id = re.compile(r'https://detail.ju.taobao.com/home.htm\?item_id=(\d+)&{0,20}.*?').findall(ju_url)[0]
                print('------>>>| 得到的淘宝商品id为:', goods_id)
                return goods_id
        else:
            print('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')
            return ''

    def __del__(self):
        gc.collect()

if __name__ == '__mian__':
    ju = JuTaobaoParse()
    while True:
        ju_url = input('请输入待爬取的淘宝商品地址: ')
        ju_url.strip('\n').strip(';')
        goods_id = ju.get_goods_id_from_url(ju_url)
        data = ju.get_goods_data(goods_id=goods_id)
        # ju.deal_with_data(goods_id=goods_id)
        # pprint(data)