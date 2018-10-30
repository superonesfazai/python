# coding = utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/8/28 20:23
@connect : superonesfazai@gmail.com
'''

# 如果是Web客户端验证，需要添加 auth = (账户名, 密码)
import requests

auth=('test', '123456')

response = requests.get('http://192.168.199.107', auth = auth)

print(response.text)