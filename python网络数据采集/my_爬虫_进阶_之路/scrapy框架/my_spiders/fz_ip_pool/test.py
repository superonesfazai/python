# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.internet_utils import get_random_phone_ua
import requests

url = "https://www.baidu.com/"

headers = {
    'Connection': "keep-alive",
    'Cache-Control': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "BAIDUID=D668B34BE04D9BF359FB05917F1E1340:FG=1; locale=zh; BIDUPSID=D668B34BE04D9BF359FB05917F1E1340; PSTM=1533542047; delPer=0; pgv_pvi=6583286784; BD_HOME=0; BD_UPN=123253; H_PS_PSSID=26524_1436_25809_21099_22157",
    'Postman-Token': "e4874f87-faef-43a4-a904-ce2ff3a4dafb"
    }

response = requests.request("GET", url, headers=headers, proxies={'http': 'http://187.4.110.58:21776'})
print(response.content.decode('utf-8'))
