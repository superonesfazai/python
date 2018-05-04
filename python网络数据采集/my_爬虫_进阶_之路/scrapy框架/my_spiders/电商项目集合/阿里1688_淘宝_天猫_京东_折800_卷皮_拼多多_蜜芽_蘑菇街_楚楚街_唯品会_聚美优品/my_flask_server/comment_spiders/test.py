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
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'accept': 'application/json, text/plain, */*',
    # 'referer': 'https://th5.m.zhe800.com/h5/comment/list?zid=ze180424214500488079&dealId=39890410&tagId=',
    # 'cookie': 'gr_user_id=84b21fed-0302-46e0-a01a-f8f3d4cb223e; session_id=439012875.1524042625; user_id=; utm_csr_first=direct; utm_csr=direct; utm_ccn=notset_c0; utm_cmd=; utm_ctr=; utm_cct=; utm_etr=tao.home; firstTime=2018-04-20; __utmz=148564220.1524192137.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); qd_user=96713570.1524192142912; frequency=1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0; lastTime=2018-04-28; unix_time=1524881786; ju_version=0; __utma=148564220.212449404.1524192137.1524208015.1524881786.3; __utmc=148564220; cart_mark=1%7C0%7C0%7Cnil%7C0; user_type=0; user_role=4; student=0; dialog_time=2; downloadGuide_config=%257B%25220direct%2522%253A%257B%2522open%2522%253A2%257D%252C%25221002direct%2522%253A%257B%2522open%2522%253A1%257D%257D; f_jk_r=https://m.zhe800.com/mz/list/wireless3982; source=; platform=; version=; channelId=; deviceId=; userId=; cType=; cId=; dealId=; f_jk=6628971525400935425TfActXWw; f_jk_t=1525400935426; f_jk_e_t=1527992935; jk=6628971525400935425TfActXWw; wris_session_id=1145460586.1525400937; visit=18',
}

params = (
    ('productId', 'ze180424214500488079'),
    ('tagId', ''),
    ('page', '1'),
    ('perPage', '20'),
)

# response = requests.get(_url, headers=headers, params=params)
# body = response.text

_url = 'https://th5.m.zhe800.com/app/detail/comment/list'
body = MyRequests.get_url_body(url=_url, headers=headers, params=params)
print(body)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://th5.m.zhe800.com/app/detail/comment/list?productId=ze180424214500488079&tagId=&page=1&perPage=20', headers=headers)
