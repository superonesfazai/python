# coding = utf-8

'''
@author = super_fazai
@File    : 最基本的get请求可以直接用get方法.py
@Time    : 2017/8/28 17:54
@connect : superonesfazai@gmail.com
'''

import requests

response = requests.get('http://www.baidu.com')

# 也可以这么写
# response = requests.request('get', 'http://www.baidu.com')
print(response.content.decode())