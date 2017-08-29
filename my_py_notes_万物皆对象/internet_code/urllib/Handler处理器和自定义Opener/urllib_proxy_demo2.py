# coding = utf-8

'''
@author = super_fazai
@File    : urllib_proxy_demo2.py
@Time    : 2017/8/28 11:27
@connect : superonesfazai@gmail.com
'''

"""
随机代理访问网站测试
"""

import urllib.request
import random

proxy_list = [
    {'http': '60.12.227.208:80'},
    {'http': '218.26.219.186:8080'},
    {'http': '222.68.207.11:80'},
    {'http': '61.53.137.50:8080'},
    {'http': '221.204.246.116:3128'},
]

proxy = random.choice(proxy_list)   # 随机选个代理

# 构建对应代理处理器对象
http_proxy_handler = urllib.request.ProxyHandler(proxy)

opener = urllib.request.build_opener(http_proxy_handler)
request = urllib.request.Request('http://www.baidu.com/')
response = opener.open(request)
print(response.read().decode())