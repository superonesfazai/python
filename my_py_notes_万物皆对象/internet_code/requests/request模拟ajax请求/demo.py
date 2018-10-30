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
    # 'Cookie': 'UM_distinctid=16015e04f6d4ff-037c1f4e36bf3-17386d57-fa000-16015e04f6e555; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; munb=2242024317; _m_user_unitinfo_=unit|unzbyun; _m_unitapi_v_=1508566261407; v=0; _tb_token_=bd731a300e5e; ali_apache_id=11.228.45.44.1512376392548.274581.5; uc3=sg2=WqJ5CclAaAIRL%2BjSIx%2FSzyVuMbp8JSBthJSylPIhcsc%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBzLQKaueubXgKyDU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTUxMjM3NjQ0MQ%3D%3D; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; cookie2=218fc7ff98e02b9b3b9d2ef572476d78; skt=9bcb2c42ae393326; t=567b173f0709a9279b1255b8cb39b2fc; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; mt=ci=46_1; l=Anl5F-hiGIwSg0yWkdu/9YJLCf5Thm05; cna=ZyWpEl+kTywCAXHXsSxv8Ati; uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=V32FPkk%2FhoypzrZtAqoZbA%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&pas=0&cookie14=UoTdeYfNor4zFg%3D%3D&tag=8&lng=zh_CN; _m_h5_tk=10ad695b4a06112d34171b6ed2493ad1_1512383470756; _m_h5_tk_enc=0da6ca6192a52175276247cd6ef5a528; CNZZDATA1000004168=140314194-1512347497-https%253A%252F%252Fwww.taobao.com%252F%7C1512381415; isg=Ap-foBPNOXPiHz1oFntdmg6ULvXprPLCRrP-SzHsO86VwL9COdSD9h2W9mZF',
}

tmp_url = 'https://guang.taobao.com/street/ajax/get_guang_list.json?_input_charset=utf-8&cpage=1&start=1&_tb_token_=bd731a300e5e&_ksTS=1512382359042_177'
response = requests.get(tmp_url, headers=headers)
body = response.content.decode('utf-8')
print(body)
