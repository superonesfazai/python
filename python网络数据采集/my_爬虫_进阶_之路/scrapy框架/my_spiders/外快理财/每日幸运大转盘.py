# coding:utf-8

'''
@author = super_fazai
@File    : 每日幸运大转盘.py
@connect : superonesfazai@gmail.com
'''

"""
外快理财幸运大转盘 ops 工具:
    每日一次机会, 分享wx后还有一次
"""

from pprint import pprint
from fzutils.spider.fz_requests import Requests
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,)

def turn_one_time() -> dict:
    cookies = {
        'Hm_lpvt_fa0ddec29ac177a2d127cebe209832e3': str(datetime_to_timestamp(get_shanghai_time())),
        'Hm_lvt_fa0ddec29ac177a2d127cebe209832e3': '1537161510,1537228200,1537353114,1537411854',       # 定值
        'wk_': '9umq63s8g6leobk2p285frmp583nhm9t',                                                      # 定值
    }
    headers = {
        'Host': 'm.riyiwk.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': 'https://m.riyiwk.com',
        'referer': 'https://m.riyiwk.com/lottery.html?check_login=1',
        'accept-language': 'zh-cn',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f/RIYIWK 2.6.0/USER_ID 203793/TOKEN 3a3988e07be98db064a70fc635c0b590',
    }
    url = 'https://m.riyiwk.com/lottery/start.html'
    res = json_2_dict(Requests.get_url_body(method='post', use_proxy=False, url=url, headers=headers, cookies=cookies))
    # pprint(res)

    return res

def share_2_wx() -> bool:
    '''
    分享给微信
    :return:
    '''
    cookies = {
        'wk_': '8llgqrevckd0bmllcdgrtqjv88elq3fl',
    }
    headers = {
        'Host': 'ios.riyiwk.com',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'ExtraIncome/2.6.0 (iPhone; iOS 11.0; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    }
    data = 'data=6FutSNjTIN512XBvPZXgztwPxRaLLFygqXFrzxnaSHhKJ0RMskgPCJ1veAFe71DmE/Weqi3qbl9Jp%2BWfhSSCtlPnKIheoydBjmxWvUtEh9qV4RXkSil0AWr5P5f8V4jL/OnQQxXgTeOBhhsJK7140Iuc/kdtw0qP'

    url = 'https://ios.riyiwk.com//user/shareCallback'
    message = json_2_dict(Requests.get_url_body(method='post', use_proxy=False, url=url, headers=headers, cookies=cookies, data=data)).get('message', '')
    label, res = ('+', True,) if message == '成功' else ('-', False,)
    print('[{}] 分享微信成功!'.format(label))

    return res

def main():
    _ = turn_one_time()
    pprint(_)
    res = share_2_wx()
    if res:
        _ = turn_one_time()
        pprint(_)
    else:
        print('模拟第二次转动转盘失败!')

    return

if __name__ == '__main__':
    main()


