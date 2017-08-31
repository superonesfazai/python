# coding = utf-8

'''
@author = super_fazai
@File    : json_dumps.py
@Time    : 2017/8/30 15:30
@connect : superonesfazai@gmail.com
'''

'''
json.dumps() 实现python类转换为json字符串, 返回一个str对象 把一个python对象编码转换为json字符串
'''

import json
import chardet

listStr = [1, 2, 3, 4]
tupleStr = (1, 2, 3, 4)
dictStr = {"city": "北京", "name": "大猫"}

json.dumps(listStr)
# '[1, 2, 3, 4]'
json.dumps(tupleStr)
# '[1, 2, 3, 4]'

# 注意：json.dumps() 序列化时默认使用的ascii编码
# 添加参数 ensure_ascii=False 禁用ascii编码，按utf-8编码

print(json.dumps(dictStr))
# '{"city": "\u5317\u4eac", "name": "\u5927\u5218"}'

# chardet是一个非常优秀的编码识别模块，可通过pip安装
# chardet.detect()返回字典, 其中confidence是检测精确度
print(chardet.detect(json.dumps(dictStr).encode()))
# {'confidence': 1.0, 'encoding': 'ascii'}

print(json.dumps(dictStr, ensure_ascii=False))
# {"city": "北京", "name": "大刘"}

print(chardet.detect(json.dumps(dictStr, ensure_ascii=False).encode()))
# {'confidence': 0.99, 'encoding': 'utf-8'}
