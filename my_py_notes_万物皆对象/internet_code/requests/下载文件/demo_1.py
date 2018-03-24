# coding:utf-8

'''
@author = super_fazai
@File    : demo_1.py
@Time    : 2018/3/22 22:33
@connect : superonesfazai@gmail.com
'''

"""
常规小文件下载
"""

import requests

image_url = 'https://avatars3.githubusercontent.com/u/23206773?s=460&v=4'

r = requests.get(image_url)
with open('./images/image_1.png', 'wb') as f:
    f.write(r.content)