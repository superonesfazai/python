# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')
from my_requests import MyRequests

# img_url 在e里
# var e = this.props.el;
# arguments里面

import requests

cookies = {
    '_9755xjdesxxd_': '32',
    'aliyungf_tc': 'AQAAAGWJOASCuwUAj7TXcatD4+ZAWQ0M',
    'acw_tc': 'AQAAALiwgjmqvAUAj7TXcbfu55yo66Zo',
    'gdxidpyhxdE': 'CJ28%5CGNcsdSXmzUTHdVSev6nZ1yjKl%5Cvxh0zhMkobdG5X1KSUMcLPw%2F2yiME13NV0VBKSEB%2FG4J38xO7bKu6zt%2B%5C%5CYNqVS0xAmEPBI5TPXth7SIKfI3y5766%2BprYd%2By%2BviSapyAayxWzzQp0k%5CWJBo0MzseMd0SbUOBf8w8tCCzrzbp5%3A1531192508207',
}

headers = {
    'Origin': 'http://www.sto.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://www.sto.cn/Home/Index',
    'X-Requested-With': 'XMLHttpRequest',
    'Proxy-Connection': 'keep-alive',
}

data = [
  ('billCodes', '3367154640058'),
  ('onClick', '1'),
  ('requestIp', '113.215.180.143, 120.27.173.13'),
  ('authCode', '3bd7d451337146d1a76e93f7f98001ab'),
  ('NECaptchaValidate', 'WkE2zVPtr8dRwFK1W.TZ8sSAGDuxFkb2BEaeDWIcRGL7wGvXoGYGWloVNUGpwXSGEFSuHF74MMR6BdOiCCNFp9OFXX0bl5I1KHSpsXNuY4qPvPIQKXHv8al1BI592QYZ01-SIZw1vhCptvnvXjyAL.XJZ0902nsNWr.ia1h.cSCd2maUhhaNrCQjsKOV.gUPC7PYOe4D.oGrWf08JKBXfoQAqUhM6YzmkKfanAeLs5LBDgQjhhK7.BqLVfk8XEtv-1aIWCbjPQaiIZ0J6yojE9FokmaPMmueUDTZKkwq1MxD0BRKCq4Vorj6t8Lhf9JDLErZZaslQGY7McOaXiIDW9vq2T1uNscOVYPMjRowSy11s._O-zbMlAUOj6aIFmBb5YoW2xwuriNiNS.iz2wSTihfuSzvJyNCxHBFzy-CDfwSazspAt1h4UpOdCHl0mZug22f2sLvlKFIHgEbtOu_Wllwo5oT6vBxeeuYkYPCwA.sQ8J8l0Yk9qiZTJr3'),
]

response = requests.post('http://www.sto.cn/Track/CheckBillCode', headers=headers, cookies=None, data=data)
print(response.text)