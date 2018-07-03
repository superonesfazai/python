# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/7/3 17:50
@connect : superonesfazai@gmail.com
'''

import wget

url = 'https://haitao.nosdn1.127.net/imq35qx294_800_800.jpg'
file_name = wget.download(url)
print(file_name)