# coding = utf-8

'''
@author = super_fazai
@File    : 获取ajax加载的内容.py
@Time    : 2017/8/27 23:18
@connect : superonesfazai@gmail.com
'''

"""
有些网页内容使用ajax加载, ajax一般返回的是json
直接对ajax地址进行post或者get，就返回数据了
"""

'''
作为一名爬虫工程师，你最需要关注的，是数据的来源
'''
import urllib.parse
import urllib.request

# demo1

url = "https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action"

headers={
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
}

# 变动的是这两个参数，从start开始往后显示limit个
formdata = {
    'start':'0',
    'limit':'10'
}
data = urllib.parse.urlencode(formdata)

request = urllib.request.Request(url, data = data, headers = headers)
response = urllib.request.urlopen(request)

print(response.read())

# demo2

url = "https://movie.douban.com/j/chart/top_list?"
headers={
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
}
# 处理所有参数
formdata = {
    'type':'11',
    'interval_id':'100:90',
    'action':'',
    'start':'0',
    'limit':'10'
}
data = urllib.parse.urlencode(formdata)

request = urllib.request.Request(url, data = data, headers = headers)
response = urllib.request.urlopen(request)

print(response.read())