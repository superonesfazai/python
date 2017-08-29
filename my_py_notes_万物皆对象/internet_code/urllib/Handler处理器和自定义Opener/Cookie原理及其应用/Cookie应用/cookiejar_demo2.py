# coding = utf-8

'''
@author = super_fazai
@File    : cookielib_demo2.py
@Time    : 2017/8/28 16:16
@connect : superonesfazai@gmail.com
'''

"""
访问网站获得cookie，并把获得的cookie保存在cookie文件中
"""

from http import cookiejar
import urllib.request

file_name = 'cookie.txt'    #保存cookie的本地磁盘文件名

# 声名一个MozillaCookieJar(有save实现)对象实例来保存cookie,之后写入文件
cookiejar = cookiejar.MozillaCookieJar(file_name)

# 使用HTTPCookieProcessor()创建cookie处理器对象, 参数为CookieJar对象
handler = urllib.request.HTTPCookieProcessor(cookiejar)

# 构建opener
opener = urllib.request.build_opener(handler)

# 创建一个请求
response = opener.open('http://www.baidu.com')

# 保存cookie到本地文件中
cookiejar.save()