# coding:utf-8

'''
@author = super_fazai
@File    : test_basic_data.py
@Time    : 2017/11/14 16:22
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from settings import BASIC_APP_KEY

import requests
import re

def test():
    while True:
        tmp_url = input('请输入待采集的url地址: ')
        tmp_url = re.compile(';').sub('', tmp_url)
        data = {
            'basic_app_key': BASIC_APP_KEY,
            'goodsLink': tmp_url,
        }

        # url = 'http://spider.taobao.k85u.com/'
        # url = 'http://0.0.0.0:5000/basic_data'
        # url = 'http://spider.other.k85u.com/basic_data'
        url = 'http://23.239.0.250/basic_data'


        headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

        response = requests.post(url, data=data, headers=headers)

        print(response.text)

        # 如果是json文件可以直接显示
        # print(response.json())

        # data = {
        #     'basic_app_key': 'yiuxiu6688',
        #     'goodsLink': 你的地址,
        # }

test()