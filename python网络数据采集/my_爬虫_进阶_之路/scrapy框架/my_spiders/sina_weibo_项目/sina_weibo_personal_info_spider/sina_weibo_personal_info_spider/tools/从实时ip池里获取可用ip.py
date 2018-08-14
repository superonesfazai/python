# coding:utf-8

'''
@author = super_fazai
@File    : 清空ip池.py
@Time    : 2017/9/25 21:07
@connect : superonesfazai@gmail.com
'''

import requests
from pprint import pprint

base_url = 'http://127.0.0.1:8000'
result = requests.get(base_url).json()

result_ip_list = {}
result_ip_list['http'] = []
for item in result:
    tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
    result_ip_list['http'].append(tmp_url)
pprint(result_ip_list)

print(len(result_ip_list['http']))

'''
删除过期代理ip
'''
def get_info_and_delete_ip():
    base_url = 'http://127.0.0.1:8000'
    result = requests.get(base_url).json()

    delete_url = 'http://127.0.0.1:8000/delete?ip='

    for item in result:
        if item[2] < 8:
            delete_info = requests.get(delete_url + item[0])
            print(delete_info.text)

get_info_and_delete_ip()