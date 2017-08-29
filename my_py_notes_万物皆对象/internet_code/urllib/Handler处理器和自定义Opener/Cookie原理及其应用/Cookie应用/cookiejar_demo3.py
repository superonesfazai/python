# coding = utf-8

'''
@author = super_fazai
@File    : cookielib_demo3.py
@Time    : 2017/8/28 16:24
@connect : superonesfazai@gmail.com
'''

"""
从文件中获取cookies,作为请求的一部分去访问
"""

from http import cookiejar
import urllib.request

# 创建MozillaCookieJar(有load实现)实例对象
cookiejar = cookiejar.MozillaCookieJar()

# 从文件中读取cookie内容到变量
cookiejar.load('cookie.txt')

handler = urllib.request.HTTPCookieProcessor(cookiejar)

opener = urllib.request.build_opener(handler)

response = opener.open('http://www.baidu.com')

print(response.read().decode())