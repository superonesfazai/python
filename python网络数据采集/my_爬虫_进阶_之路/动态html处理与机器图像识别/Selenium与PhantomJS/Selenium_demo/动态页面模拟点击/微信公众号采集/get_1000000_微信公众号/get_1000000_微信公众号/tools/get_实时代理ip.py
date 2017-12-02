# coding:utf-8

'''
@author = super_fazai
@File    : get_实时代理ip.py
@Time    : 2017/9/25 19:29
@connect : superonesfazai@gmail.com
'''

"""
得到实时代理ip
"""

from urllib import request, parse
import json
from pprint import pprint

# print('send data....')
showapi_appid = "46819"  # 替换此值
showapi_sign = "98bfbd4d3b2b438c9d53edc498a1e202"  # 替换此值
url = "http://route.showapi.com/22-1"
send_data = parse.urlencode([
    ('showapi_appid', showapi_appid),
    ('showapi_sign', showapi_sign)
])

req = request.Request(url)
try:
    response = request.urlopen(req, data=send_data.encode('utf-8'), timeout=6)  # 10秒超时反馈

    result = response.read().decode('utf-8')
    result_json = json.loads(result)
    # print('返回的json数据为:', result_json)

    result_content_list = result_json['showapi_res_body']['pagebean']['contentlist']
    # print(result_content_list)

    deal_with_result = []
    for item in result_content_list:
        tmp_result = 'http://' + str(item['ip']) + ':' +str(item['port'])
        deal_with_result.append(tmp_result)
    pprint(deal_with_result)
except Exception as e:
    print(e)


