# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from fzutils.spider.fz_requests import MyRequests
from fzutils.internet_utils import get_random_pc_ua

import requests

headers = {
    'cookie': 'cna=2svqE2mvXBoCAXHXtPCLe5oQ; ali_ab=113.215.181.173.1533958807673.5; hng=CN%7Czh-CN%7CCNY%7C156; enc=m%2BjS1LgMF1GDKdZ%2Bk9XOequkk88LCLXaWl6ahSVlh8w6bVx%2FkMy1xi8ayUvf%2BNnYNAKIKFCsCuJPyxxP6s%2FN9A%3D%3D; JSESSIONID=t2xYwgg-vl9aRX09Cv8bz9qOXB-mLnr31R-0BLC1; t=8f06ca31d89f46259fd1468bf31f8403; _tb_token_=e136a3858b373; lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA; __cn_logon__=false; h_keys="2018%u5973%u88c5%u8fde%u8863%u88d9#2018%u534a%u8eab%u88d9%u5973%u88c5"; ctoken=opaAtmE7EqUnjgxBPo48naga; __cn_logon__.sig=i6UL1cVhdIpbPPA_02yGiEyKMeZR2hBfnaoYK1CcrF4; _tmp_ck_0=IlQ2M6x9F5wUZn6CY9fN%2Ft4X35QhH%2BjmAmOfSPBfR5XMiwRDKxHkZ%2FflvG9lTatz63qcir%2Bc8OlfxAebngePG1hpeTWHvgM4uC%2FbV4mEK%2FgQTTVXoogTKg3FzKmxBLsU6hrAiRj1Nimcr06EHlAp722N4izUbqPZzEI1sBG3uh6GDqBdJ0NCOtBXUwffiHus1T6GlXQvSDlOuvKv9J4Q4yB8%2Bjjq1bSjxY0EdVqWAzEiKqNApBaWGZig7drkCEiPs2bNmXidMMmczWOncFouUGtYU9EReebWUqVGHvHvrqLf6tKVNzX4JM4kClzuXgL%2FgolmlKpfSMV1GKx2cKwMT3FwgK04FhA5LsENr0yxCXnmeRMP9WuY9KIUq12gC7v0UcL5IB8PDP4%3D; ad_prefer="2018/08/28 09:30:11"; _csrf_token=1535966655772; alicnweb=homeIdttS%3D00024041126239256510087946013720426621%7Ctouch_tb_at%3D1535966735147; ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiJOQkNLLWQzRXRpTU1NamstQmRGRkRUdGsiLCJfZXhwaXJlIjoxNTM2MDUzMTkyMzg1LCJfbWF4QWdlIjo4NjQwMDAwMH0=; ali-ss.sig=8KlYN2mffe__5YrHnH2af2bKZM1x3iiFQ8emi7QDMew; _m_h5_tk=cc02038f1131670b24d3d06b776dccba_1535976153536; webp=1; isg=BL-_Rj8f2HrjhtyEGyvifAs8TpWJDBEgeVSX-lGMam7gYN7iWXV_lyo2pjCeOOu-',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    # 'referer': 'https://m.1688.com/page/offerRemark.htm?offerId=533755145596',
    'authority': 'm.1688.com',
    'x-requested-with': 'XMLHttpRequest',
}

params = (
    ('_csrf', 'Lbjsw9C7-kZajGpmwEpSkiJpyki8tSQHk05o'),
    ('__wing_navigate_type', 'view'),
    ('__wing_navigate_url', 'detail:modules/offerRemarkList/view'),
    ('__wing_navigate_options', '{"data":{"offerId":"533755145596","receiveUserId":2875117712,"starLevel":7,"itemId":533755145596,"bizType":"trade","page":1,"pageSize":5}}'),
    # ('_', '1535966808899'),
)

response = requests.get('https://m.1688.com/page/offerRemark.htm', headers=headers, params=params)
print(response.text)