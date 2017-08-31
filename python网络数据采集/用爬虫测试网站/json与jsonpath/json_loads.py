# coding = utf-8

'''
@author = super_fazai
@File    : json_loads.py
@Time    : 2017/8/30 15:21
@connect : superonesfazai@gmail.com
'''

"""
json.loads() 把Json格式字符串解码转换成Python对象
"""

import json

str_list = '[1, 2, 3, 4]'
str_dict = '{"city": "北京", "name": "大猫"}'

print(json.loads(str_list))     # loads的第一个参数可以传入a str or byte or bytearray instance containing a JSON document) to a Python object.

print(json.loads(str_dict))    # json数据自动按unicode存储


'''
测试结果:
[1, 2, 3, 4]
{'city': '北京', 'name': '大猫'}
'''