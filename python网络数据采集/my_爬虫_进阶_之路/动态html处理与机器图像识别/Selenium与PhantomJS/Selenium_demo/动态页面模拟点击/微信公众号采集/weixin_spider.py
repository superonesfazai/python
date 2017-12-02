# coding:utf-8

'''
@author = super_fazai
@File    : weixin_spider.py
@Time    : 2017/1/23 20:25
@connect : superonesfazai@gmail.com
'''

"""
获取某微信公众号所有文章
"""

import requests
import redis
import json
import re
import random
import time
from pprint import pprint

'''
给与该公众号的id
'''
# gzlist = ['sogaad']
gzlist = ['superonesfazai']
# gzlist = ['henizaiyiqisjz']

url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }

with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie = f.read()
cookies = json.loads(cookie)
response = requests.get(url=url, cookies=cookies)
token = re.findall(r'token=(\d+)', str(response.url))[0]
print(token)
for query in gzlist:
    query_id = {
        'action': 'search_biz',
        'token' : token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '5',
    }
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'

    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
    tmp_url = search_response.url   # 构造结果url
    print(tmp_url)
    lists = search_response.json().get('list')[0]
    print(lists)

    fakeid = lists.get('fakeid')
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    tmp_url2 = appmsg_response.url
    print(tmp_url2)
    max_num = appmsg_response.json().get('app_msg_cnt')     # 发布的文章总数
    article_lists = appmsg_response.json().get('app_msg_list')   # 发布的文章lists
    pprint(article_lists)

    # # 下面注释掉的是进行提取文章的代码
    num = int(int(max_num) / 5)
    begin = 0
    while num + 1 > 0 :
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        print('翻页###################',begin)
        query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        for item in fakeid_list:
            print(item.get('link'))
        num -= 1
        begin = int(begin)
        begin+=5
        time.sleep(2)