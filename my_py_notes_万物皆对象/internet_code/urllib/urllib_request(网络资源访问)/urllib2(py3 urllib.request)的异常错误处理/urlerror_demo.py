# coding = utf-8

'''
@author = super_fazai
@File    : urlerror_demo.py
@Time    : 2017/8/28 17:24
@connect : superonesfazai@gmail.com
'''

"""
我们可以用try except语句来捕获相应的异常。
下面的例子里我们访问了一个不存在的域名
"""

import urllib.request
from urllib.error import URLError

request = urllib.request.Request('http://www.ajkfhafwjqh.com')

try:
    urllib.request.urlopen(request, timeout=5)
except URLError as err:
    print(err)

'''
urlopen error，错误代码8，错误原因是没有找到指定的服务器。
'''