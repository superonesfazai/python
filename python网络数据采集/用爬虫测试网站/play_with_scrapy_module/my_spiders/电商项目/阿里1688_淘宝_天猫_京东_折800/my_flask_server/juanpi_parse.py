# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_parse.py
@Time    : 2017/11/17 17:26
@connect : superonesfazai@gmail.com
'''

"""
卷皮页面采集系统
"""

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal
from time import sleep
import datetime
import re
import gc
import pytz

from settings import HEADERS

class JuanPiParse(object):
    def __init__(self):
        super(JuanPiParse, self).__init__()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'web.juanpi.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            return {}
        else:
            tmp_url = 'https://web.juanpi.com/pintuan/shop/' + str(goods_id)
            print('------>>>| 得到的商品手机版的地址为: ', tmp_url)

            # 设置代理ip
            self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
            self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

            tmp_proxies = {
                'http': self.proxy,
            }
            # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

            try:
                response = requests.get(tmp_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                data = response.content.decode('utf-8')
                # print(data)
                data = re.compile(r'__PRELOADED_STATE__=(.*),window.').findall(data)  # 贪婪匹配匹配所有
                # print(data)
            except Exception:
                print('requests.get()请求超时....')
                print('data为空!')
                return {}

            if data != []:
                data = data[0]
                try:
                    data = json.loads(data)
                except:
                    return {}
                # pprint(data)

                if data.get('detail') is not None:
                    data = data.get('detail', {})
                    # 处理commitments
                    try:
                        data['commitments'] = ''
                        data.get('discount', {})['coupon'] = ''
                        data.get('discount', {})['coupon_index'] = ''
                        data.get('discount', {})['vip_info'] = ''
                        data['topbanner'] = ''
                    except:
                        pass
                    pprint(data)

                else:
                    print('data中detail的key为None, 返回空dict')
                    return {}
            else:
                print('data为空!')
                return {}

    def deal_with_data(self):
        pass

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

    def get_goods_id_from_url(self, juanpi_url):
        '''
        得到goods_id
        :param juanpi_url:
        :return: goods_id (类型str)
        '''
        is_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/.*?').findall(juanpi_url)
        if is_juanpi_url != []:
            if re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url) != []:
                tmp_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                if tmp_juanpi_url != '':
                    goods_id = tmp_juanpi_url
                else:   # 只是为了在pycharm运行时不调到chrome，其实else完全可以不要的
                    juanpi_url = re.compile(r';').sub('', juanpi_url)
                    goods_id = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)
                print('------>>>| 得到的卷皮商品的地址为:', goods_id)
                return goods_id

        else:
            print('卷皮商品url错误, 非正规的url, 请参照格式(http://shop.juanpi.com/deal/)开头的...')
            return ''

if __name__ == '__main__':
    juanpi = JuanPiParse()
    while True:
        zhe_800_url = input('请输入待爬取的卷皮商品地址: ')
        zhe_800_url.strip('\n').strip(';')
        goods_id = juanpi.get_goods_id_from_url(zhe_800_url)
        data = juanpi.get_goods_data(goods_id=goods_id)
        juanpi.deal_with_data()