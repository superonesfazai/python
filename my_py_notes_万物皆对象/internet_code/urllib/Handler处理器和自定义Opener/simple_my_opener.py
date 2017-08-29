# coding = utf-8

'''
@author = super_fazai
@File    : simple_my_opener.py
@Time    : 2017/8/28 10:51
@connect : superonesfazai@gmail.com
'''

"""
简单的自定义opener()
"""

import urllib.request

# 构建一个HTTPHandler处理对象, 支持处理HTTP请求
http_handler = urllib.request.HTTPHandler(debuglevel=1)

# 调用urllib.request.build_opener()方法, 创建支持处理http请求的opener对象
opener = urllib.request.build_opener(http_handler)

# 构建Request请求
request = urllib.request.Request('http://www.baidu.com/')

# 调用自定义的opener对象的open()方法,发送request请求
response = opener.open(request)

# 获取服务器响应的内容
print(response.read().decode())

# 这种方式发送请求得到的结果，和使用urllib2.urlopen()发送HTTP/HTTPS请求得到的结果是一样的

'''
如果在 HTTPHandler()增加 debuglevel=1参数，
还会将 Debug Log 打开，这样程序在执行的时候，
会把收包和发包的报头在屏幕上自动打印出来，方便调试，
有时可以省去抓包的工作

# 仅需要修改的代码部分：

# 构建一个HTTPHandler 处理器对象，支持处理HTTP请求，同时开启Debug Log，debuglevel 值默认 0
http_handler = urllib.request.HTTPHandler(debuglevel=1)

# 构建一个HTTPHSandler 处理器对象，支持处理HTTPS请求，同时开启Debug Log，debuglevel 值默认 0
https_handler = urllib.request.HTTPSHandler(debuglevel=1)
'''