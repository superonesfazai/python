# coding:utf-8

'''
@author = super_fazai
@File    : 测试跨域下载img.py
@connect : superonesfazai@gmail.com
'''

import requests

IMAGE_URL = 'https://pic.7y7.com/Uploads/Picture/2019-07-05/5d1eba0f819f1_450_0.jpg'

def request_download():
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Sec-Fetch-Mode': 'navigate',
    }
    r = requests.get(
        url=IMAGE_URL,
        headers=headers,)
    with open('./img2.png', 'wb') as f:
        f.write(r.content)

request_download()