# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.internet_utils import get_random_pc_ua
import requests
from requests.exceptions import (
    ConnectTimeout,
    ReadTimeout,
    ProxyError,)

headers = {
    'Connection': "keep-alive",
    'Cache-Control': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': get_random_pc_ua(),
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
}

def proxy_ip_check(url, headers, ip, port):
    '''验证proxy可用性'''
    proxies = {
        'http': 'http://{}:{}'.format(ip, port),
        'https': 'http://{}:{}'.format(ip, port),
    }
    body = ''
    try:
        response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=5)
        body = response.content.decode('utf-8')
    except (ConnectTimeout, ReadTimeout, ProxyError) as e:
        print('遇到错误: ', e.args[0])

    return body

from pickle import dumps
from fzutils.sql_utils import BaseRedisCli
from fzutils.data.pickle_utils import deserializate_pickle_object
from fzutils.safe_utils import get_uuid3
from fzutils.data.list_utils import list_remove_repeat_dict

redis_cli = BaseRedisCli()
_ = deserializate_pickle_object(redis_cli.get(get_uuid3('proxy_tasks')) or dumps([]))
_ = list_remove_repeat_dict(target=_, repeat_key='ip')

# url = 'https://www.baidu.com'
# url = 'http://127.0.0.1/get'
# url = 'https://whatleaks.com/'
url = 'http://amibehindaproxy.com/'
# body = proxy_ip_check(url=url, headers=headers, ip='125.122.151.10', port=9000)
# print(body)

import requests

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    # 'X-DevTools-Emulate-Network-Conditions-Client-Id': '82EE68AF7DC0F43BF063AE41D795B860',
}

response = requests.get('http://www.66ip.cn/2.html', headers=headers)
body = response.content.decode('gb2312')
print(body)