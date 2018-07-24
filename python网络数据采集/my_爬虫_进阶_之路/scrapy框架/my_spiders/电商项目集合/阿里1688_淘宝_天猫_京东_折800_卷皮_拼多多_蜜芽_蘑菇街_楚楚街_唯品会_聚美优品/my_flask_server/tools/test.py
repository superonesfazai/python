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

# img_url 在e里
# var e = this.props.el;
# arguments里面

import requests

url = "https://list.tmall.com/m/search_items.htm"

querystring = {"page_size":"20","page_no":"1","q":"b","type":"p","tmhkh5":"","spm":"a220m.6910245.a2227oh.d100","from":"mallfp..m_1_searchbutton"}

headers = {
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36",
    'accept': "*/*",
    # 'referer': "https://list.tmall.com/search_product.htm?q=a&type=p&tmhkh5=&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_searchbutton",
    'authority': "list.tmall.com",
    # 'cookie': "login=true;",
    'Cache-Control': "no-cache",
    # 'Postman-Token': "99786fca-5039-4bb5-981f-548b1057d456"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)