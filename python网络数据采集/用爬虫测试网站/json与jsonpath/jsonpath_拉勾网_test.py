# coding = utf-8

'''
@author = super_fazai
@File    : jsonpath_拉勾网_test.py
@Time    : 2017/8/30 16:04
@connect : superonesfazai@gmail.com
'''

import urllib.request
import jsonpath
import json
import chardet

url = 'http://www.lagou.com/lbs/getAllCitySearchLabels.json'
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

html = response.read()

# 把json格式字符串转换为python对象
json_obj = json.loads(html)

# 从根节点开始, 匹配name节点
city_list = jsonpath.jsonpath(json_obj, '$..name')

print(city_list)
print(type(city_list))
fp = open('city.json', 'w', encoding='utf-8')

content = json.dumps(city_list, ensure_ascii=False)
print(content)
fp.write(content)
fp.close()