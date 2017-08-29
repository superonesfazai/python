# coding = utf-8

'''
@author = super_fazai
@File    : urllib_proxy_demo1.py
@Time    : 2017/8/28 11:09
@connect : superonesfazai@gmail.com
'''

"""使用自定义opener来使用代理"""

import urllib.request

# 构建2个代理Handler,一个有代理ip, 一个没有
http_proxy_handler = urllib.request.ProxyHandler({'http': '124.88.67.81:80'})
null_proxy_handler = urllib.request.ProxyHandler({})

proxy_switch = True # 定义一个代理开关

# 通过urllib.request.build_opener()方法使用这些代理Handler对象
# 创建自定义opener对象
if proxy_switch:
    opener = urllib.request.build_opener(http_proxy_handler)
else:
    opener = urllib.request.build_opener(null_proxy_handler)

request = urllib.request.Request('http://www.baidu.com/')

# 1. 如果这么写，只有使用opener.open()方法发送请求才使用自定义的代理
#    而urlopen()则不使用自定义代理。
response = opener.open(request)

# 2. 如果这么写，就是将opener应用到全局，
#    之后所有的，不管是opener.open()还是urlopen() 发送请求，都将使用自定义代理。
# urllib.request.install_opener(opener)
# response = urlopen(request)

print(response.read().decode())

