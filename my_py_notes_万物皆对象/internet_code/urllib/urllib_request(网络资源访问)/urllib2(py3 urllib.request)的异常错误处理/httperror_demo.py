# coding = utf-8

'''
@author = super_fazai
@File    : httperror_demo.py
@Time    : 2017/8/28 17:30
@connect : superonesfazai@gmail.com
'''

import urllib.request
from urllib.error import HTTPError

requset = urllib.request.Request('http://blog.baidu.com/itcast')

try:
    urllib.request.urlopen(requset)
except HTTPError as err:
    print(err.code)
    print(err)