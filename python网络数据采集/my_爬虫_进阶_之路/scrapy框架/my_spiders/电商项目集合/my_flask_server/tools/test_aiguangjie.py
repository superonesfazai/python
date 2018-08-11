# coding:utf-8

'''
@author = super_fazai
@File    : test_aiguangjie.py
@Time    : 2017/12/4 12:36
@connect : superonesfazai@gmail.com
'''

# http://acs.m.taobao.com/h5/mtop.taobao.phenix.h5index.get/2.0/?appKey=12574478&api=mtop.taobao.phenix.h5index.get&v=2.0&type=originaljson&dataType=jsonp

import requests
import time
from random import randint
import json
import re
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import gc

'''
测试一: 模拟获取爱逛街mobile端接口
'''
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'acs.m.taobao.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Cookie': 'UM_distinctid=16015e04f6d4ff-037c1f4e36bf3-17386d57-fa000-16015e04f6e555; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; ockeqeudmj=jJgePkU%3D; munb=2242024317; WAPFDFDTGFG=%2B4cMKKP%2B8PI%2Buj7zjGYZ%2FmcrTpFkcttXbzWPw1Gvbiu%2F; _w_app_lg=17; _m_user_unitinfo_=unit|unzbyun; _m_unitapi_v_=1508566261407; ali_apache_id=11.228.45.44.1512376392548.274581.5; uc3=sg2=WqJ5CclAaAIRL%2BjSIx%2FSzyVuMbp8JSBthJSylPIhcsc%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBzLQKaueubXgKyDU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; cookie2=218fc7ff98e02b9b3b9d2ef572476d78; t=567b173f0709a9279b1255b8cb39b2fc; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; mt=ci=46_1; l=Anl5F-hiGIwSg0yWkdu/9YJLCf5Thm05; cna=ZyWpEl+kTywCAXHXsSxv8Ati; miid=5767446262036433919; v=0; _tb_token_=bd731a300e5e; uc1=cookie14=UoTdeYA%2B9w4Ojw%3D%3D; _m_h5_tk=219735eaad3d8781ae971b3e2ae27208_1512453593695; _m_h5_tk_enc=f39bbd9adc9b5c18b23b9eee8363bac7; isg=AiMjFtYHfSzMlTEcctcZVmKgsmENsLYgPMZhC1WAfwL5lEO23ehHqgHE_l5l',
    'Referer': 'http://market.m.taobao.com/apps/guang/ishopping/new_index.html',
}

appKey = '12574478'
t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
# sign = 'e460083bcee46a037f7ed32cc1b5d31b'
# data:{"pageNo":1,"pageSize":10,"sceneStatus":"","popupQuery":"index"}
'''
下面是构造params
'''
data = {
    'pageNo': 1,
    'pageSize': 10,
    'sceneStatus': '',
    'popupQuery': 'index',
}
params = {
    'data': json.dumps(data),
}

# http://acs.m.taobao.com/h5/mtop.taobao.phenix.h5index.get/2.0/?appKey=12574478&t=1512369242325&sign=d35f00ce371f854be49eea1b05f48d0c&api=mtop.taobao.phenix.h5index.get&v=2.0&type=originaljson&dataType=jsonp
url = 'http://acs.m.taobao.com/h5/mtop.taobao.phenix.h5index.get/2.0/?appKey={0}&t={1}&api=mtop.taobao.phenix.h5index.get&v=2.0&type=originaljson&dataType=jsonp'.format(
    appKey, t,
)
# response = requests.get(url=url, headers=headers, params=params)
response = requests.post(url=url, data=json.dumps(params), headers=headers)
print(response.url)
# last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
# print(last_url)
# response = requests.get(last_url, headers=headers, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
body = response.content.decode('utf-8')
print(body)

print('*' * 100)

'''
测试二: 模拟ajax爱逛街pc端接口
'''
############################### requests模拟ajax请求
headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'guang.taobao.com',
    # 'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://guang.taobao.com/',      # 必须的参数
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    # 'Cookie': 'UM_distinctid=16015e04f6d4ff-037c1f4e36bf3-17386d57-fa000-16015e04f6e555; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; munb=2242024317; _m_user_unitinfo_=unit|unzbyun; _m_unitapi_v_=1508566261407; v=0; _tb_token_=bd731a300e5e; ali_apache_id=11.228.45.44.1512376392548.274581.5; uc3=sg2=WqJ5CclAaAIRL%2BjSIx%2FSzyVuMbp8JSBthJSylPIhcsc%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBzLQKaueubXgKyDU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTUxMjM3NjQ0MQ%3D%3D; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; cookie2=218fc7ff98e02b9b3b9d2ef572476d78; skt=9bcb2c42ae393326; t=567b173f0709a9279b1255b8cb39b2fc; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; mt=ci=46_1; l=Anl5F-hiGIwSg0yWkdu/9YJLCf5Thm05; cna=ZyWpEl+kTywCAXHXsSxv8Ati; uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=V32FPkk%2FhoypzrZtAqoZbA%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&pas=0&cookie14=UoTdeYfNor4zFg%3D%3D&tag=8&lng=zh_CN; _m_h5_tk=10ad695b4a06112d34171b6ed2493ad1_1512383470756; _m_h5_tk_enc=0da6ca6192a52175276247cd6ef5a528; CNZZDATA1000004168=140314194-1512347497-https%253A%252F%252Fwww.taobao.com%252F%7C1512381415; isg=Ap-foBPNOXPiHz1oFntdmg6ULvXprPLCRrP-SzHsO86VwL9COdSD9h2W9mZF',
}

tmp_url = 'https://guang.taobao.com/street/ajax/get_guang_list.json?_input_charset=utf-8&cpage=1&start=1&_tb_token_=bd731a300e5e&_ksTS=1512382359042_177'
response2 = requests.get(tmp_url, headers=headers2)
body2 = response2.content.decode('utf-8')
print(body2)



