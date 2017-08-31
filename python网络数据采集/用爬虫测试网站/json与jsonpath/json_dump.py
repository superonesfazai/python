# coding = utf-8

'''
@author = super_fazai
@File    : json_dump.py
@Time    : 2017/8/30 15:48
@connect : superonesfazai@gmail.com
'''

"""
json.dump() 将python内置类型序列化为json对象后写入文件
"""

import json

listStr = [{"city": "北京"}, {"name": "大刘"}]
print(json.dump(listStr, open("listStr.json","w", encoding='utf-8'), ensure_ascii=False))

dictStr = {"city": "北京", "name": "大刘"}
print(json.dump(dictStr, open("dictStr.json","w", encoding='utf-8'), ensure_ascii=False))
