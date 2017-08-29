# coding = utf-8

'''
@author = super_fazai
@File    : 添加headers和查询参数.py
@Time    : 2017/8/28 17:58
@connect : superonesfazai@gmail.com
'''

"""
如果想添加headers,可以传入headers参数来增加请求头中的headers信息
如果要将参数放到url中传递, 可以利用params参数
"""

import requests

kw = {'wd': '长城'}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

# params接收一个字典或者字符串的查询参数
# 字典类型自动转换为url编码, 不需要urlencode()
response = requests.get('http://www.baidu.com/s?', params=kw, headers=headers)

# 查看响应内容, response.txt返回的是unicode格式的数据
print(response.text)

# 查看响应内容, response.content返回的是字节流数据
print(response.content)

# 查看完整url地址
print(response.url)

# 查看响应头部字符编码
print(response.encoding)

# 查看响应码
print(response.status_code)