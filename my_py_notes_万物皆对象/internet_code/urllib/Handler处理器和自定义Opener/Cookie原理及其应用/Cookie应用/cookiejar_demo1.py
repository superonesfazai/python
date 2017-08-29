# coding = utf-8

'''
@author = super_fazai
@File    : cookielib_demo1.py
@Time    : 2017/8/28 16:00
@connect : superonesfazai@gmail.com
'''

"""
获取Cookie, 并保存到CookieJar对象中
"""

import urllib.request
from http import cookiejar       # cookielib模块在python3中已经改名为http.cookiejar了

cookiejar = cookiejar.CookieJar()   # 构建一个Cookie对象来保存cookie

# 使用HTTPCookieProcessor()来构造对象, 参数为Cookiejar()对象
handler = urllib.request.HTTPCookieProcessor(cookiejar)

# 构建一个opener
opener = urllib.request.build_opener(handler)

# 以get方式访问页面, 访问之后自动保存cookie到cookiejar中
opener.open('http://www.baidu.com')

# 按标准的格式将保存的Cookie打印出来
cookie_str = ''
for item in cookiejar:
    cookie_str = cookie_str + item.name + '=' + item.value + ';'

# 舍去最后一位的分号
print(cookie_str[:-1])



