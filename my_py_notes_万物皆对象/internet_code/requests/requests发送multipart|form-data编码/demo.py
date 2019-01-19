# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
requests发送multipart/form-data编码
"""

# 发送文件中的数据
from requests_toolbelt import MultipartEncoder
import requests

data = MultipartEncoder(
    fields={
        'field0': 'value',
        'field1': 'value',
        # 'field2': ('filename', open('__init__.py', 'rb'), 'text/plain')
    })
headers = {
    'Content-Type': data.content_type,
}
url = 'http://httpbin.org/post'
r = requests.post(
    url=url,
    data=data,
    headers=headers)
print(r.text)