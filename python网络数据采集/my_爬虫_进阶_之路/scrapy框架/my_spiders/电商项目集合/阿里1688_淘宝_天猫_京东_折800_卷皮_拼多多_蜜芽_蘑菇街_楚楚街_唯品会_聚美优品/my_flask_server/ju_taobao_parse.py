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
import gc
# import pycurl
# from io import StringIO
# import traceback
# from io import BytesIO

from settings import PHANTOMJS_DRIVER_PATH, CHROME_DRIVER_PATH

from fzutils.internet_utils import get_random_pc_ua

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
            'User-Agent': get_random_pc_ua(),      # 随机一个请求头
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

        # 手机版地址
        phone_url = 'https://ju.taobao.com/m/jusp/alone/detailwap/mtp.htm?item_id=' + str(goods_id)
        print('------>>>| 该商品对应手机端地址: ', phone_url)

        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        try:
            response = requests.get(tmp_url, headers=self.headers, params=params, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
            # print(last_url)
            response = requests.get(last_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            data = response.content.decode('utf-8')
            # print(data)
            data = re.compile(r'define\((.*)\)').findall(data)  # 贪婪匹配所有
            # print(data)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            return {}

        if data != []:
            data = data[0]
            data = json.loads(data)
            # pprint(data)

            # 处理商品被转移或者下架导致页面不存在的商品
            if data.get('data').get('seller', {}).get('evaluates') is None:
                print('data为空, 地址被重定向, 该商品可能已经被转移或下架')
                return {}

            data['data']['rate'] = ''  # 这是宝贝评价
            data['data']['resource'] = ''  # 买家询问别人
            data['data']['vertical'] = ''  # 也是问和回答
            data['data']['seller']['evaluates'] = ''  # 宝贝描述, 卖家服务, 物流服务的评价值...
            result_data = data['data']

            # 处理result_data['apiStack'][0]['value']
            # print(result_data.get('apiStack', [])[0].get('value', ''))
            result_data_apiStack_value = result_data.get('apiStack', [])[0].get('value', {})
            try:
                result_data_apiStack_value = json.loads(result_data_apiStack_value)

                result_data_apiStack_value['consumerProtection'] = ''  # 7天无理由退货
                result_data_apiStack_value['feature'] = ''
                result_data_apiStack_value['layout'] = ''
                result_data_apiStack_value['delivery'] = ''  # 发货地到收到地
                result_data_apiStack_value['resource'] = ''  # 优惠券
                result_data_apiStack_value['item'] = ''
                # pprint(result_data_apiStack_value)
            except Exception:
                print("json.loads转换出错，得到result_data['apiStack'][0]['value']值可能为空，此处跳过")
                result_data_apiStack_value = ''
                pass

            # 将处理后的result_data['apiStack'][0]['value']重新赋值给result_data['apiStack'][0]['value']
            result_data['apiStack'][0]['value'] = result_data_apiStack_value

            # 处理mockData
            mock_data = result_data['mockData']
            mock_data = json.loads(mock_data)
            mock_data['feature'] = ''
            # pprint(mock_data)
            result_data['mockData'] = mock_data

            # print(result_data.get('apiStack', [])[0])   # 可能会有{'name': 'esi', 'value': ''}的情况
            if result_data.get('apiStack', [])[0].get('value', '') == '':
                print("result_data.get('apiStack', [])[0].get('value', '')的值为空....")
                result_data['trade'] = {}
                return {}
            else:
                result_data['trade'] = result_data.get('apiStack', [])[0].get('value', {}).get('trade', {})  # 用于判断该商品是否已经下架的参数
                # pprint(result_data['trade'])

            self.result_data = result_data
            pprint(self.result_data)
            return  result_data
        else:
            print('data为空!')
            return {}

    def deal_with_data(self, goods_id):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = data['seller'].get('shopName', '')  # 可能不存在shopName这个字段

            # 掌柜
            account = data['seller'].get('sellerNick', '')

            # 商品名称
            title = data['item']['title']
            # 子标题
            sub_title = data['item'].get('subtitle', '')
            sub_title = re.compile(r'\n').sub('', sub_title)
            # 店铺主页地址
            # shop_name_url = 'https:' + data['seller']['taoShopUrl']
            # shop_name_url = re.compile(r'.m.').sub('.', shop_name_url)  # 手机版转换为pc版

            # 商品价格
            # price = data['apiStack'][0]['value']['price']['extraPrices'][0]['priceText']
            tmp_taobao_price = data['apiStack'][0].get('value', '').get('price').get('price').get('priceText', '')
            tmp_taobao_price = tmp_taobao_price.split('-')  # 如果是区间的话，分割成两个，单个价格就是一个
            # print(tmp_taobao_price)
            if len(tmp_taobao_price) == 1:
                # 商品最高价
                # price = Decimal(tmp_taobao_price[0]).__round__(2)     # json不能处理decimal所以后期存的时候再处理
                price = tmp_taobao_price[0]
                # 商品最低价
                taobao_price = price
                # print(price)
                # print(taobao_price)
            else:
                # price = Decimal(tmp_taobao_price[1]).__round__(2)
                # taobao_price = Decimal(tmp_taobao_price[0]).__round__(2)
                price = tmp_taobao_price[1]
                taobao_price = tmp_taobao_price[0]
                # print(price)
                # print(taobao_price)

            print('最高价: ', price, '最低价: ', taobao_price)

            # 淘宝价
            # taobao_price = data['apiStack'][0]['value']['price']['price']['priceText']
            # taobao_price = Decimal(taobao_price).__round__(2)

        else:
            print('待处理的data为空的dict, 该商品可能已经转移或者下架')
            # return {
            #     'is_delete': 1,
            # }
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
                print('------>>>| 得到的聚划算商品id为:', goods_id)
                return goods_id
            else:       # 处理存数据库中取出的如: https://detail.ju.taobao.com/home.htm?item_id=560164926470
                print('9999')
                ju_url = re.compile(r';').sub('', ju_url)
                goods_id = re.compile(r'https://detail.ju.taobao.com/home.htm\?item_id=(\d+)&{0,20}.*?').findall(ju_url)[0]
                print('------>>>| 得到的聚划算商品id为:', goods_id)
                return goods_id
        else:
            print('聚划算商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')
            return ''

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    ju = JuTaobaoParse()
    while True:
        ju_url = input('请输入待爬取的聚划算商品地址: ')
        ju_url.strip('\n').strip(';')
        goods_id = ju.get_goods_id_from_url(ju_url)
        data = ju.get_goods_data(goods_id=goods_id)
        ju.deal_with_data(goods_id=goods_id)
        # pprint(data)