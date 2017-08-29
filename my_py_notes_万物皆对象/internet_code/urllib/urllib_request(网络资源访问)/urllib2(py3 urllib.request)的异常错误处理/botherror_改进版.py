# coding = utf-8

'''
@author = super_fazai
@File    : botherror_改进版.py
@Time    : 2017/8/28 17:34
@connect : superonesfazai@gmail.com
'''

"""
这样我们就可以做到，
首先捕获子类的异常，
如果子类捕获不到，那么可以捕获父类的异常。
"""

import urllib.request
from urllib.error import HTTPError, URLError

requset = urllib.request.Request('http://blog.baidu.com/itcast')

try:
    urllib.request.urlopen(requset)

except HTTPError as err:
    print(err.code)

except URLError as err:
    print(err)

else:
    print("Good Job")