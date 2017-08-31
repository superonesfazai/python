# coding = utf-8

'''
@author = super_fazai
@File    : json_load.py
@Time    : 2017/8/30 15:53
@connect : superonesfazai@gmail.com
'''

"""
json.load() 读取文件中json形式的字符串元素 转换为python类型
"""

import json

str_list = json.load(open('./listStr.json', encoding='utf-8'))
print(str_list)

str_dict = json.load(open('./dictStr.json', encoding='utf-8'))
print(str_dict)

'''
测试结果:
[{'city': '北京'}, {'name': '大刘'}]
{'city': '北京', 'name': '大刘'}
'''