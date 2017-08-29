# coding = utf-8

'''
@author = super_fazai
@File    : 私密代理.py
@Time    : 2017/8/28 20:21
@connect : superonesfazai@gmail.com
'''
import requests
# 如果代理需要使用HTTP Basic Auth，可以使用下面这种格式：
proxy = { "http": "mr_mao_hacker:sffqry9r@61.158.163.130:16816" }

response = requests.get("http://www.baidu.com", proxies = proxy)

print(response.text)