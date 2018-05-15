# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

# m
a = [
    (1, 75),
    (2, 80),
    (2, 60),
    (1, 88),
    (2, 70),
    (1.5, 63),
    (4, 63),
    (1.5, 73),
    (1.5, 60),
    (2, 68),
    (3, 61),
    (1, 60),
    (1, 85),
    (3, 70),
    (1, 70),
    (3.5, 66),
    (4, 78),
    (1, 90),
    (3, 87),
    (4, 71),
    (3, 84),
    (1, 85),
    (1, 85),
    (2.5, 81),
    (1.5, 78),
    (2, 95),
    (2, 69),
    (1.5, 86),
    (2.5, 87),
    (1, 95),
    (3, 81),
    (2, 90),
    (1, 89),
    (1, 85),
    (5.5, 82),
    (5.5, 70),
    (2.5, 65),
    (3, 60),
    (1.5, 67),
    (1.5, 68),
    (3.5, 71),
    (4.5, 79),
    (4, 61),
    (4, 72),
    (1.5, 76),
    (1.5, 76),
    (1.5, 77),
    (1.5, 67),
    (3, 75),
    (3, 73),
    (6, 78),
    (2, 73),
    (.25, 60),

    # (3.5, 60),
    # (3, 60),
    # (3, 60),
    # (4, 60),
    (3.5, 33),
    (3, 53),
    (3, 43),
    (4, 51),
]

# 任
b = [
    (1, 75),
    (2, 83),
    (2, 62),
    (1, 90),
    (2, 77),
    (1.5, 73),
    (3.5, 61),
    (4, 60),
    (1.5, 73),
    (1.5, 70),
    (2, 80),
    (3, 70),
    (3, 66),
    (1, 70),
    (1, 65),
    (3, 77),
    (1, 70),
    (3.5, 79),
    (4, 78),
    (1, 70),
    (3, 77),
    (4, 75),
    (1, 75),
    (1, 65),
    (1.5, 60),
    (2, 75),
    (2, 92),
    (1.5, 92),
    (2.5, 82),
    (1., 75),
    (3, 84),
    (2, 90),
    (1, 93),
    (1, 91),
    (5.5, 63),
    (2.5, 62),
    (4, 61),
    (3, 60),
    (1.5, 65),
    (1.5, 70),
    (3.5, 64),
    (4.5, 60),
    (4, 69),
    (4,  64),
    (1.5, 82),
    (1.5, 82),
    (1.5, 76),
    (1.5, 77),
    (3, 84),
    (3, 69),
    (6, 73),
    (2, 77),
    (.25, 95),

    (3, 60),
    (2.5, 60),
    (5.5, 60),
    (3, 50),
]

# 王
c = [
    (1, 75),
    (2, 89),
    (1, 68),
    (2, 73),
    (1.5, 67),
    (3.5, 61),
    (4, 63),
    (1.5, 73),
    (1.5, 60),
    (2, 74),
    (3, 63),
    (1, 60),
    (1, 65),
    (3, 67),
    (1, 60),
    (3.5, 60),
    (4, 68),
    (1, 60),
    (3, 84),
    (4, 82),
    (3, 69),
    (1, 75),
    (1, 70),
    (1.5, 60),
    (2, 75),
    (2, 90),
    (1.5, 88),
    (2.5, 79),
    (1, 75),
    (3, 82),
    (2, 72),
    (1, 69),
    (5.5, 60),
    (5.5, 73),
    (3, 60),
    (1.5, 68),
    (1.5, 71),
    (3.5, 61),
    (4.5, 63),
    (4, 69),
    (4, 64),
    (1.5, 80),
    (1.5, 81),
    (1.5, 87),
    (1.5, 60),
    (3, 83),
    (3, 69),
    (6, 74),
    (2, 69),
    (.25, 91),

    (2, 60),
    (3, 60),
    (2.5, 60),
    (1, 60),
    (2.5, 60),
    (3, 60),
    (4, 60),
]

_i = 0.
_sum = 0.
for item in a:
    _i += item[0]
    _sum += item[0]*item[1]

# print(_sum/_i)
# print(len(a), len(b), len(c))

import sys
sys.path.append('..')
import requests
from my_requests import MyRequests

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'accept': '*/*',
    'referer': 'https://g.zhe800.com/xianshiqiang/index',
    'authority': 'zapi.zhe800.com',
    # 'cookie': 'gr_user_id=84b21fed-0302-46e0-a01a-f8f3d4cb223e; session_id=439012875.1524042625; user_id=; utm_csr_first=direct; utm_csr=direct; utm_ccn=notset_c0; utm_cmd=; utm_ctr=; utm_cct=; utm_etr=tao.home; firstTime=2018-04-20; __utmz=148564220.1524192137.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); qd_user=96713570.1524192142912; __utmc=148564220; user_type=0; user_role=4; student=0; source=; platform=; version=; channelId=; deviceId=; userId=; cType=; cId=; dealId=; wris_session_id=1145460586.1525400937; f_jk_r=https://m.zhe800.com/mz/list/wireless3982; f_jk=8578391525402580084TfActXWw; f_jk_t=1525402580085; f_jk_e_t=1527994580; jk=8578391525402580084TfActXWw; frequency=1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0; lastTime=2018-05-15; unix_time=1526354956; ju_version=0; cart_mark=1%7C0%7C0%7Cnil%7C0; __utma=148564220.212449404.1524192137.1524881786.1526354957.4; __utmt=1; __utmb=148564220.1.10.1526354957; visit=49; dialog_time=1; downloadGuide_config=%257B%25220direct%2522%253A%257B%2522open%2522%253A5%257D%252C%25221002direct%2522%253A%257B%2522open%2522%253A3%257D%257D',
}

params = (
    # ('new_user', ['0', '0']),
    ('session_id', '18130'),
    ('page', '1'),
    # ('source', 'h5'),
    ('per_page', '20'),
    # ('callback', 'getXianshiSessionDataCallBack18130'),
)

# response = requests.get('https://zapi.zhe800.com/zhe800_n_api/xsq/m/session_deals', headers=headers, params=params)
# print(response.text)

_url = 'https://zapi.zhe800.com/zhe800_n_api/xsq/m/session_deals'
body = MyRequests.get_url_body(url=_url, headers=headers, params=params)
print(body)
