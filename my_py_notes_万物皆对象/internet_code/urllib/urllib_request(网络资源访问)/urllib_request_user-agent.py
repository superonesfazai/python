# coding = utf-8

'''
@author = super_fazai
@File    : urllib_request_user-agent.py
@Time    : 2017/8/27 20:16
@connect : superonesfazai@gmail.com
'''

import urllib.request

url = 'http://www.google.com'
#IE 9.0 的 User-Agent，包含在 ua_header里
ua_header = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
}

# # * 随机添加/修改User-Agent
# ua_list = [
#     "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
#     "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
#     "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS... ",
# ]
# import random
# user_agent = random.choice(ua_list)
# request = urllib.request.Request(url)
# # 也可以通过调用Request.add_header() 添加/修改一个特定的header
# request.add_header("User-Agent", user_agent)
# # 第一个字母大写，后面的全部小写
# request.get_header("User-agent")

# url连同headers, 一起构造Request请求, 这个请求将附带IE 9.0 的user-agent
request = urllib.request.Request(url, headers=ua_header)

# 添加更多的Header信息
# 也可以通过调用Request.add_header() 添加/修改一个特定的header
request.add_header("Connection", "keep-alive")

# 也可以通过调用Request.get_header()来查看header信息
# request.get_header(header_name="Connection")

response = urllib.request.urlopen(request)
from pprint import pprint
pprint(response.read().decode())



