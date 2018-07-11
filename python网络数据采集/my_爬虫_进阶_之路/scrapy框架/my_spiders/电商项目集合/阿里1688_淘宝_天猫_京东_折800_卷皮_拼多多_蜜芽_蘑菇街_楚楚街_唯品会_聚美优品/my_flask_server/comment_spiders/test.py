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
from my_utils import _get_url_contain_params

import requests

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'accept': '*/*',
    # 'referer': 'https://item.taobao.com/item.htm?id=555788234147',
    'authority': 'rate.taobao.com',
    # 'cookie': 't=1bdcbe0b678123e1755897be375b453f; cna=UOK9Ey4N1hYCAXHXtRx8QV37; thw=cn; enc=b5TkGZ7%2F21TQIJJszNV9Lh6NcqQo2HsiX8RUxdH1xWxdk1bDmUu4bwcp%2FdmRjjjgULSKAfJQPasgu2nWMNNlnw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cookie2=34038e4edfe48b5b4098bc3b078d5fb7; v=0; _tb_token_=e6ebd3be3e5ae; _m_h5_tk=95ce2ae2b7a1bd2a07e7a340701154e2_1531291260140; _m_h5_tk_enc=1f3e30a146f42c44ea2bb082f5c05d30; uc1=cookie14=UoTfKjY967l2dA%3D%3D; mt=ci%3D-1_0; isg=BMzMlnq5-1klje_VIiqTC5W_nSxSrR9PTMFGMiaNt3cxsW67ThTvPhFDVPks2qgH',
}

params = (
    ('auctionNumId', '555788234147'),
    # ('userNumId', '2503579154'),
    ('currentPageNum', '1'),
    ('pageSize', '20'),
    ('rateType', '1'),
    ('orderType', 'sort_weight'),
    ('attribute', ''),
    ('sku', ''),
    ('hasSku', 'false'),
    ('folded', '0'),
    # ('ua', '098#E1hv0vvWvP6vUvCkvvvvvjiPPszW1jtjn2qWAj1VPmPp1jEhPFS9QjtPnLFvtj3WdphvHs9hl98YSpCWUGeARADWzw066XOqUZzh2QhvCvvvMMGEvpCWvCr8vvw/aNBraB4AVAdvaNLvHdBYLWFvQWp7RAYVyO2vqbVQWl4vgRFE+FIlBqevD70fderv+8c61CA4wxzXS47BhC3qVUcnDOmwjOyCvvOUvvVCayVivpvUvvmvW+DmPKRtvpvIvvvvk6CvvjpvvvjIphvUsQvv99CvpvAvvvvmGZCv2mpvvvb1phvWEvhCvvOvCvvvphvtvpvhvvvvv8wCvvpvvUmm3QhvCvvhvvmCvpv44HrxvPsw7Di4wX2N8IFpQqMBw6Hu9amq1I+tvpvhvvvvvv=='),
    # ('_ksTS', '1531315988314_1250'),
    # ('callback', 'jsonp_tbcrate_reviews_list'),
)

response = requests.get('https://rate.taobao.com/feedRateList.htm', headers=headers, params=params)
print(response.text)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://rate.taobao.com/feedRateList.htm?auctionNumId=555788234147&userNumId=2503579154&currentPageNum=1&pageSize=20&rateType=1&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098%23E1hv0vvWvP6vUvCkvvvvvjiPPszW1jtjn2qWAj1VPmPp1jEhPFS9QjtPnLFvtj3WdphvHs9hl98YSpCWUGeARADWzw066XOqUZzh2QhvCvvvMMGEvpCWvCr8vvw%2FaNBraB4AVAdvaNLvHdBYLWFvQWp7RAYVyO2vqbVQWl4vgRFE%2BFIlBqevD70fderv%2B8c61CA4wxzXS47BhC3qVUcnDOmwjOyCvvOUvvVCayVivpvUvvmvW%2BDmPKRtvpvIvvvvk6CvvjpvvvjIphvUsQvv99CvpvAvvvvmGZCv2mpvvvb1phvWEvhCvvOvCvvvphvtvpvhvvvvv8wCvvpvvUmm3QhvCvvhvvmCvpv44HrxvPsw7Di4wX2N8IFpQqMBw6Hu9amq1I%2Btvpvhvvvvvv%3D%3D&_ksTS=1531315988314_1250&callback=jsonp_tbcrate_reviews_list', headers=headers)
