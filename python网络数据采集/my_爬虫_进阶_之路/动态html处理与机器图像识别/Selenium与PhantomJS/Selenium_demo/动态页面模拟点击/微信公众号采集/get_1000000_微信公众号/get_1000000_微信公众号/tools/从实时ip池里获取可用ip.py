# coding:utf-8

'''
@author = super_fazai
@File    : 清空ip池.py
@Time    : 2017/9/25 21:07
@connect : superonesfazai@gmail.com
'''

import requests

base_url = 'http://127.0.0.1:8000'
result = requests.get(base_url).json()

result_ip_list = []
for item in result:
    tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
    result_ip_list.append(tmp_url)
print(result_ip_list)
