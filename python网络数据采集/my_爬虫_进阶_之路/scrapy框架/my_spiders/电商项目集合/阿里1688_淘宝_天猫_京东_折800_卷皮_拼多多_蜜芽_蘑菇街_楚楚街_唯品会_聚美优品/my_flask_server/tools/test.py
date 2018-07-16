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

url = "http://v.xiaohongshu.com/ltIHd_J-l8iV7iLCL_tMGirulVxt"

querystring = {
    "sign":"b861dbc75d0fe72f159f15be827efa36",
    "t":"5b4d785a",
}

headers = {
    'Cookie': "xhsTrackerId=96359c99-a7b3-4725-c75d-2ee052cf2cc1",
    'Accept': "*/*",
    'Connection': "keep-alive",
    'Accept-Encoding': "gzip, deflate",
    'X-Tingyun-Id': "LbxHzUNcfig;c=2;r=1687041668",
    'Host': "v.xiaohongshu.com",
    'User-Agent': "discover/5202001 CFNetwork/878.2 Darwin/17.0.0",
    'Accept-Language': "zh-cn",
    'Range': "bytes=2-6325716",
    'Cache-Control': "no-cache",
    'Postman-Token': "e67b4a4d-2642-4593-beb8-606206a89aa9"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
