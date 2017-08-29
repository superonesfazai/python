# coding = utf-8

'''
@author = super_fazai
@File    : 利用cookiejar和post登录人人网.py
@Time    : 2017/8/28 16:31
@connect : superonesfazai@gmail.com
'''

"""
利用cookiejar和post登录人人网
"""

import urllib.request
import urllib.parse
from http import cookiejar

cookie = cookiejar.CookieJar()   # 构建一个CookieJar对象实例来保存cookie

cookie_handler = urllib.request.HTTPCookieProcessor(cookie)     # 创建cookie处理对象

opener = urllib.request.build_opener(cookie_handler)    # 构建opener

# addheaders接受一个list，里面每个元素都是以一个headers信息的元组,opener将附带headers的信息
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')]

# 需要登录的账户和密码
data = {
    'email': 'mr_mao_hacker@163.com',
    'password': 'alarmchime',
}

# 通过urlencode()转码
post_data = urllib.parse.urlencode(data)

# 构建Request请求对象, 包含发送需要的用户名和密码
request = urllib.request.Request('http://www.renren.com/Plogin.do', data=post_data)

# 通过opener发送这个请求, 并获得登录后的Cookie值
opener.open(request)

# opener包含用户登录后的Cookie值，可以直接访问那些登录后才可以访问的页面
response = opener.open("http://www.renren.com/410043129/profile")

print(response.read().decode())

'''
测试案例中，为了想让大家快速理解知识点，我们使用的人人网登录接口是人人网改版前的隐藏接口(嘘....)，登录比较方便。
现在这个接口已经没用了
'''

