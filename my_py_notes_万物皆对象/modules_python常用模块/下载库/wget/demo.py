# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

import wget

url = 'https://haitao.nosdn1.127.net/imq35qx294_800_800.jpg'
file_name = wget.download(url)
print(file_name)