# coding = utf-8

'''
@author = super_fazai
@File    : cookies.py
@Time    : 2017/8/28 20:29
@connect : superonesfazai@gmail.com
'''

import requests

response = requests.get("http://www.baidu.com/")

# 7. 返回CookieJar对象:
cookiejar = response.cookies

# 8. 将CookieJar转为字典：
cookiedict = requests.utils.dict_from_cookiejar(cookiejar)

print(cookiejar)

print(cookiedict)

'''
测试结果:
<RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>
{'BDORZ': '27315'}
'''