# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/12/4 19:16
@connect : superonesfazai@gmail.com
'''

import requests

############################### requests模拟ajax请求(get)
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'guang.taobao.com',
    # 'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://guang.taobao.com/',      # 必须的参数
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    # 'Cookie': '',
}

tmp_url = 'https://guang.taobao.com/street/ajax/get_guang_list.json?_input_charset=utf-8&cpage=1&start=1&_tb_token_=bd731a300e5e&_ksTS=1512382359042_177'
response = requests.get(tmp_url, headers=headers)
body = response.content.decode('utf-8')
print(body)
